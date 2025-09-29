import fs from 'fs/promises'
import path from 'path'

import { INDEX, ensureUserBundles } from './state.js'

export function sendError(res, status, detail) {
  return res.status(status).json({ detail })
}

export function bundleOwnership(user, bid) {
  if (!INDEX.has(bid)) return { error: { status: 404, detail: 'unknown bundle' } }
  const owned = ensureUserBundles(user.userId).has(bid)
  if (!owned) return { error: { status: 403, detail: 'forbidden' } }
  return { ok: true }
}

export async function listFiles(rootDir) {
  const out = []

  async function walk(rel) {
    const current = path.join(rootDir, rel)
    const entries = await fs.readdir(current, { withFileTypes: true })
    for (const entry of entries) {
      const relPath = path.join(rel, entry.name)
      const fullPath = path.join(rootDir, relPath)
      try {
        const stat = await fs.lstat(fullPath)
        if (stat.isFile() || stat.isSymbolicLink()) out.push(relPath.replace(/^\/+/, ''))
        if (entry.isDirectory()) await walk(relPath)
      } catch (_) {
      }
    }
  }

  await walk('')
  return out.sort()
}
