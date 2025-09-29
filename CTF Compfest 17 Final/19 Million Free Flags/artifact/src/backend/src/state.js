import crypto from 'crypto'

export const INDEX = new Map()

const USERS_BY_USERNAME = new Map()
const USERS_BY_ID = new Map()
const USERS_BY_TOKEN = new Map()

const BUNDLES_BY_USER = new Map()

function randomUserId() {
  return Number(BigInt.asUintN(48, process.hrtime.bigint()))
}

function randomToken() {
  return crypto.randomBytes(16).toString('hex')
}

export function createUser({ username, password = null, displayName, role = 0, token }) {
  if (USERS_BY_USERNAME.has(username)) {
    throw new Error('username already exists')
  }
  const userId = randomUserId()
  const finalToken = token || randomToken()
  const record = { userId, username, password, displayName, role, token: finalToken }
  USERS_BY_USERNAME.set(username, record)
  USERS_BY_ID.set(userId, record)
  USERS_BY_TOKEN.set(finalToken, record)
  ensureUserBundles(userId)
  return record
}

export function upsertAnonymousUser(token) {
  if (token && USERS_BY_TOKEN.has(token)) {
    return USERS_BY_TOKEN.get(token)
  }
  const username = `anon_${crypto.randomBytes(6).toString('hex')}`
  const displayName = `Guest ${username.slice(-4)}`
  return createUser({ username, displayName, role: 0, token })
}

export function getUserByUsername(username) {
  return USERS_BY_USERNAME.get(username)
}

export function getUserById(userId) {
  return USERS_BY_ID.get(Number(userId))
}

export function getUserByToken(token) {
  return USERS_BY_TOKEN.get(token)
}

export function setUserPassword(username, password) {
  const record = USERS_BY_USERNAME.get(username)
  if (record) {
    record.password = password
  }
  return record
}

export function ensureUserBundles(userId) {
  const key = Number(userId)
  if (!BUNDLES_BY_USER.has(key)) {
    BUNDLES_BY_USER.set(key, new Set())
  }
  return BUNDLES_BY_USER.get(key)
}
