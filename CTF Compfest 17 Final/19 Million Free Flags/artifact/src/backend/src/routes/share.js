import { Router } from 'express'
import crypto from 'crypto'
import path from 'path'
import fs from 'fs/promises'
import mime from 'mime-types'

import { SHARE_SECRET, UPLOAD_ROOT } from '../config.js'
import { INDEX, ensureUserBundles } from '../state.js'
import { requireAuth } from '../middleware/auth.js'
import { sendError } from '../utils.js'

const router = Router()

function percentEncode(buffer) {
  let out = ''
  for (const byte of buffer) {
    const ch = String.fromCharCode(byte)
    if ((byte >= 0x30 && byte <= 0x39) || (byte >= 0x41 && byte <= 0x5a) || (byte >= 0x61 && byte <= 0x7a) || ch === '-' || ch === '_' || ch === '.' || ch === '~') {
      out += ch
    } else {
      out += `%${byte.toString(16).padStart(2, '0').toUpperCase()}`
    }
  }
  return out
}

function percentDecode(value) {
  const bytes = []
  for (let i = 0; i < value.length;) {
    const code = value.charCodeAt(i)
    if (code === 37 && i + 2 < value.length) {
      const chunk = value.slice(i + 1, i + 3)
      const parsed = Number.parseInt(chunk, 16)
      if (!Number.isNaN(parsed)) {
        bytes.push(parsed)
        i += 3
        continue
      }
    }
    if (code === 43) {
      bytes.push(0x20)
    } else {
      bytes.push(code & 0xff)
    }
    i += 1
  }
  return Buffer.from(bytes)
}

function parseQuery(raw) {
  const out = new Map()
  if (!raw) return out
  for (const segment of raw.split('&')) {
    if (!segment) continue
    const idx = segment.indexOf('=')
    const key = idx === -1 ? segment : segment.slice(0, idx)
    const value = idx === -1 ? '' : segment.slice(idx + 1)
    const keyBuf = percentDecode(key)
    const keyStr = keyBuf.toString('latin1')
    if (!out.has(keyStr)) out.set(keyStr, [])
    out.get(keyStr).push(percentDecode(value))
  }
  return out
}

function encodeValue(input) {
  return percentEncode(Buffer.from(String(input), 'utf8'))
}

function buildPayload(id, exp, filePath) {
  return `id=${encodeValue(id)}&exp=${encodeValue(exp)}&path=${encodeValue(filePath)}`
}

function rawQuery(req) {
  const idx = req.originalUrl.indexOf('?')
  if (idx === -1) return ''
  return req.originalUrl.slice(idx + 1)
}

router.get('/share/sign', requireAuth, (req, res) => {
  const id = typeof req.query.id === 'string' ? req.query.id : ''
  const exp = typeof req.query.exp === 'string' ? req.query.exp : ''
  const filePath = typeof req.query.path === 'string' ? req.query.path : ''
  if (!id || !exp || !filePath) return sendError(res, 400, 'missing fields')
  if (!/^\d+$/.test(exp)) return sendError(res, 400, 'invalid exp')
  if (!INDEX.has(id)) return sendError(res, 404, 'unknown bundle id')
  if (!ensureUserBundles(req.user.userId).has(id)) return sendError(res, 403, 'forbidden bundle')
  const info = INDEX.get(id)
  if (!info.files.includes(filePath)) return sendError(res, 404, 'unknown bundle path')
  const expInt = Number.parseInt(exp, 10)
  if (!Number.isFinite(expInt)) return sendError(res, 400, 'invalid exp')
  if (expInt <= Math.floor(Date.now() / 1000)) return sendError(res, 403, 'expired')
  const payload = buildPayload(id, exp, filePath)
  const payloadBuf = Buffer.from(payload, 'utf8')
  const sig = crypto.createHash('sha256').update(SHARE_SECRET).update(payloadBuf).digest('hex')
  res.json({ payload, payload_q: percentEncode(payloadBuf), sig, payload_len: payloadBuf.length })
})

router.get('/share/export', async (req, res) => {
  const top = parseQuery(rawQuery(req))
  const payloadValues = top.get('payload') || []
  const sigValues = top.get('sig') || []
  if (!payloadValues.length || !sigValues.length) return sendError(res, 400, 'missing payload/sig')
  const payloadBuf = payloadValues.at(-1)
  const sig = sigValues.at(-1).toString('ascii')
  if (!/^[0-9a-fA-F]{64}$/.test(sig)) return sendError(res, 400, 'invalid sig')
  const calc = crypto.createHash('sha256').update(SHARE_SECRET).update(payloadBuf).digest('hex')
  if (calc !== sig.toLowerCase()) return sendError(res, 403, 'bad sig')
  const payloadParams = parseQuery(payloadBuf.toString('latin1'))
  const idValues = payloadParams.get('id') || []
  const pathValues = payloadParams.get('path') || []
  const expValues = payloadParams.get('exp') || []
  if (!idValues.length || !pathValues.length) return sendError(res, 400, 'missing id/path')
  const id = idValues.at(-1).toString('utf8')
  if (!INDEX.has(id)) return sendError(res, 404, 'unknown bundle id')
  const info = INDEX.get(id)
  const expStr = expValues.length ? expValues[0].toString('utf8') : '0'
  let expInt = Number.parseInt(expStr, 10)
  if (!Number.isFinite(expInt)) expInt = 0
  if (expInt <= Math.floor(Date.now() / 1000)) return sendError(res, 403, 'expired')
  const baseCandidate = pathValues[0]
  let basePath = null
  for (const entry of info.files) {
    const entryBuf = Buffer.from(entry, 'utf8')
    if (baseCandidate.length >= entryBuf.length && baseCandidate.subarray(0, entryBuf.length).equals(entryBuf)) {
      basePath = entry
      break
    }
  }
  if (!basePath) return sendError(res, 404, 'unknown bundle path')
  const canonical = Buffer.from(buildPayload(id, expStr, basePath), 'utf8')
  if (payloadBuf.length < canonical.length || !payloadBuf.subarray(0, canonical.length).equals(canonical)) {
    return sendError(res, 400, 'invalid payload canonical form')
  }
  const targetPath = pathValues.at(-1).toString('utf8')
  const target = path.join(UPLOAD_ROOT, id, targetPath)
  try {
    await fs.access(target)
  } catch {
    return sendError(res, 404, 'not found')
  }
  const ext = path.extname(target).toLowerCase()
  const detectedMimeType = mime.lookup(ext)
  const contentType = detectedMimeType || 'text/plain; charset=utf-8'
  const filename = path.basename(target)
  return res.sendFile(target, {
    headers: {
      'Content-Disposition': `inline; filename="${filename}"`,
      'Content-Type': contentType
    }
  })
})

export default router
