const API_PREFIX = '/api'

const authHeaders = (token, extra = {}) => {
  const headers = new Headers(extra.headers || {})
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  return {
    ...extra,
    credentials: 'include',
    headers,
  }
}

export async function apiHealth() {
  const res = await fetch(`${API_PREFIX}/health`)
  if (!res.ok) throw new Error(`health ${res.status}`)
  return res.json()
}

export async function authAnonymous(existingToken) {
  const res = await fetch(`${API_PREFIX}/auth/anonymous-login`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: existingToken || null }),
  })
  if (!res.ok) throw new Error('anonymous login failed')
  return res.json()
}

export async function authRegister({ username, password, displayName }) {
  const res = await fetch(`${API_PREFIX}/auth/register`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, displayName }),
  })
  if (!res.ok) {
    throw new Error(await res.text().catch(() => 'register failed'))
  }
  return res.json()
}

export async function authLogin({ username, password }) {
  const res = await fetch(`${API_PREFIX}/auth/login`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) {
    throw new Error(await res.text().catch(() => 'login failed'))
  }
  return res.json()
}

export async function authLogout() {
  await fetch(`${API_PREFIX}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  }).catch(() => {})
}

export async function authMe() {
  const res = await fetch(`${API_PREFIX}/auth/me`, {
    credentials: 'include',
  })
  if (!res.ok) throw new Error('not authenticated')
  return res.json()
}

export async function escalateRole(secret) {
  const res = await fetch(`${API_PREFIX}/auth/escalate`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret }),
  })
  if (!res.ok) {
    throw new Error(await res.text().catch(() => 'escalation failed'))
  }
  return res.json()
}

export async function listBundles(token) {
  const res = await fetch(`${API_PREFIX}/bundles`, authHeaders(token))
  if (!res.ok) throw new Error(await res.text().catch(() => 'list failed'))
  return res.json()
}

export async function uploadBundle(file, token) {
  const fd = new FormData()
  fd.append('archive', file)
  const res = await fetch(`${API_PREFIX}/bundles`, {
    method: 'POST',
    body: fd,
    credentials: 'include',
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  })
  if (!res.ok) {
    const t = await res.text().catch(() => '')
    throw new Error(`upload failed: ${res.status} ${t}`)
  }
  return res.json()
}


const encodePath = (p) => p.split('/').map(encodeURIComponent).join('/')

export async function fetchFileBlob(id, filePath, token) {
  const res = await fetch(`${API_PREFIX}/file/${encodeURIComponent(id)}/${encodePath(filePath)}`, authHeaders(token))
  if (!res.ok) {
    const t = await res.text().catch(() => '')
    throw new Error(`file fetch failed: ${res.status} ${t}`)
  }
  const blob = await res.blob()
  return { blob, contentType: res.headers.get('content-type') || 'application/octet-stream' }
}

export async function signShare({ id, path, expEpoch }) {
  const qs = new URLSearchParams()
  qs.set('id', id)
  qs.set('path', path)
  qs.set('exp', String(expEpoch))
  const res = await fetch(`${API_PREFIX}/share/sign?${qs.toString()}`, { credentials: 'include' })
  if (!res.ok) throw new Error('sign failed')
  return res.json()
}

export function buildShareUrl({ id, path, expEpoch }) {
  return signShare({ id, path, expEpoch }).then(({ payload_q: payloadQ, sig }) => `${API_PREFIX}/share/export?payload=${payloadQ}&sig=${sig}`)
}

// Internal API functions (admin only)
export async function searchBundles(keyword = '') {
  const qs = new URLSearchParams()
  if (keyword) qs.set('keyword', keyword)
  const res = await fetch(`${API_PREFIX}/internal/search?${qs.toString()}`, {
    credentials: 'include'
  })
  if (!res.ok) throw new Error(await res.text().catch(() => 'search failed'))
  return res.json()
}

export async function getBundleFiles(bundleId) {
  const res = await fetch(`${API_PREFIX}/internal/bundle/${encodeURIComponent(bundleId)}/files`, {
    credentials: 'include'
  })
  if (!res.ok) throw new Error(await res.text().catch(() => 'failed to get bundle files'))
  return res.json()
}

export async function downloadInternalFile(bundleId, filePath, saveAs = null) {
  const qs = new URLSearchParams()
  if (saveAs) qs.set('saveAs', saveAs)
  const url = `${API_PREFIX}/internal/bundle/${encodeURIComponent(bundleId)}/download/${encodeURIComponent(filePath)}?${qs.toString()}`
  const res = await fetch(url, {
    credentials: 'include'
  })
  if (!res.ok) throw new Error(await res.text().catch(() => 'download failed'))
  const blob = await res.blob()
  return { blob, contentType: res.headers.get('content-type') || 'application/octet-stream' }
}
