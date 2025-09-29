import { getUserById, getUserByToken } from '../state.js'
import { verifySession } from '../session.js'
import { sendError } from '../utils.js'

export function requireAuth(req, res, next) {
  let user = null

  const cookieSession = req.cookies && req.cookies.session
  if (cookieSession) {
    const session = verifySession(cookieSession)
    if (session) {
      const record = getUserById(session.userId)
      if (record) {
        user = record
        user.role = session.role
      }
    }
  }

  if (!user) {
    const header = req.get('authorization') || ''
    if (!header.startsWith('Bearer ')) {
      return sendError(res, 401, 'missing credentials')
    }
    const token = header.slice(7).trim()
    const record = getUserByToken(token)
    if (!record) {
      return sendError(res, 403, 'forbidden')
    }
    user = record
  }

  req.user = user
  req.authToken = user.token
  return next()
}
