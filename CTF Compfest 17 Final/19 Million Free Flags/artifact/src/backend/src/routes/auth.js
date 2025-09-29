import { Router } from 'express'

import {
  createUser,
  getUserByUsername,
  upsertAnonymousUser,
} from '../state.js'
import { requireAuth } from '../middleware/auth.js'
import { clearSessionCookie, setSessionCookie } from '../session.js'
import { sendError } from '../utils.js'

const router = Router()

router.post('/anonymous-login', (req, res) => {
  const provided = req.body && typeof req.body.token === 'string' ? req.body.token : null
  const user = upsertAnonymousUser(provided)
  setSessionCookie(res, user)
  res.json({ username: user.username, token: user.token })
})

router.post('/register', (req, res) => {
  const { username, password, displayName } = req.body || {}
  if (typeof username !== 'string' || username.length < 3) {
    return sendError(res, 400, 'username must be at least 3 characters')
  }
  if (typeof password !== 'string' || password.length < 4) {
    return sendError(res, 400, 'password must be at least 4 characters')
  }
  const name = typeof displayName === 'string' && displayName.length > 0 ? displayName : username
  if (name.length > 20) {
    return sendError(res, 400, 'display name too long')
  }
  if (getUserByUsername(username)) {
    return sendError(res, 409, 'username already exists')
  }
  const user = createUser({ username, password, displayName: name, role: 0 })
  setSessionCookie(res, user)
  res.json({ username: user.username, token: user.token })
})

router.post('/login', (req, res) => {
  const { username, password } = req.body || {}
  if (typeof username !== 'string' || typeof password !== 'string') {
    return sendError(res, 400, 'missing credentials')
  }
  const user = getUserByUsername(username)
  if (!user || user.password !== password) {
    return sendError(res, 401, 'invalid credentials')
  }
  setSessionCookie(res, user)
  res.json({ username: user.username, token: user.token })
})

router.post('/logout', (req, res) => {
  clearSessionCookie(res)
  res.json({ ok: true })
})

router.get('/me', requireAuth, (req, res) => {
  const user = req.user
  res.json({
    username: user.username,
    displayName: user.displayName,
    role: user.role,
    token: user.token,
  })
})

router.patch('/me', requireAuth, (req, res) => {
  const { displayName } = req.body || {}
  if (typeof displayName !== 'string' || displayName.length === 0) {
    return sendError(res, 400, 'display name required')
  }

  if (displayName.length > 20) {
    return sendError(res, 400, 'display name too long')
  }
  
  const user = req.user
  user.displayName = displayName
  
  setSessionCookie(res, user)
  res.json({
    username: user.username,
    displayName: user.displayName,
    role: user.role,
    token: user.token,
  })
})

router.post('/escalate', requireAuth, (req, res) => {
  const { secret } = req.body || {}
  const expectedSecret = process.env.SECRET
  
  if (secret === expectedSecret) {
    const user = req.user
    user.role = 1
    
    setSessionCookie(res, user)
    res.json({
      username: user.username,
      displayName: user.displayName,
      role: user.role,
      token: user.token,
      message: 'Role escalated to administrator'
    })
  } else {
    return sendError(res, 403, 'invalid escalation key')
  }
})

export default router
