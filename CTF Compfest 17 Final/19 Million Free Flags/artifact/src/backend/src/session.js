import { createRequire } from 'module'
import crypto from 'crypto'

const require = createRequire(import.meta.url)

const authNative = require('../native/auth/build/Release/auth.node')

const SESSION_SECRET = crypto.randomBytes(32).toString('hex')
const secretBuffer = Buffer.from(SESSION_SECRET, 'utf8')

function base64UrlDecode(data) {
  const normalized = data.replace(/-/g, '+').replace(/_/g, '/')
  const padLength = (4 - (normalized.length % 4)) % 4
  const padded = normalized + '='.repeat(padLength)
  return Buffer.from(padded, 'base64')
}

function base64UrlEncode(buffer) {
  return Buffer.from(buffer).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_')
}

export function issueSession(user) {
  const payload = {
    userId: user.userId,
    role: user.role,
    name: user.displayName,
  }
  const tokenBuffer = authNative.issue(secretBuffer, payload)
  return base64UrlEncode(tokenBuffer)
}

export function setSessionCookie(res, user) {
  const token = issueSession(user)
  res.cookie('session', token, { httpOnly: true, sameSite: 'lax', path: '/' })
  return token
}

export function clearSessionCookie(res) {
  res.clearCookie('session', { path: '/' })
}

export function verifySession(token) {
  try {
    const buffer = base64UrlDecode(token)
    const session = authNative.verify(secretBuffer, buffer)
    return session
  } catch (error) {
    return null
  }
}
