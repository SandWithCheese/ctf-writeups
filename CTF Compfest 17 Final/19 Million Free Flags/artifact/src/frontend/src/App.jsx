import React, { useEffect, useState } from 'react'

import {
  apiHealth,
  authAnonymous,
  authLogin,
  authLogout,
  authRegister,
  authMe,
} from './api.js'
import { Bundles } from './components/Bundles.jsx'
import { BundleView } from './components/BundleView.jsx'
import { TopBar } from './components/TopBar.jsx'
import { UploadCard } from './components/UploadCard.jsx'
import { AdminPanel } from './components/AdminPanel.jsx'
import { RoleEscalation } from './components/RoleEscalation.jsx'
import { useToken } from './hooks/useToken.js'

export default function App() {
  const { token, setToken, clear } = useToken()
  const [healthy, setHealthy] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)
  const [selected, setSelected] = useState(null)
  const [user, setUser] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiHealth().then(() => setHealthy(true)).catch(() => setHealthy(false))
  }, [])

  useEffect(() => {
    authMe().then((me) => {
      setUser(me)
      // Backend v2 uses session cookies, token is still available for display
      if (me.token) setToken(me.token)
    }).catch(() => {
      setUser(null)
    })
  }, [])

  const refreshSession = async () => {
    try {
      const me = await authMe()
      setUser(me)
      if (me.token) setToken(me.token)
      setError('')
      return me
    } catch (e) {
      setUser(null)
      throw e
    }
  }

  const doAnonymous = async () => {
    setError('')
    try {
      const { token: newToken } = await authAnonymous(token || undefined)
      if (newToken) setToken(newToken)
      await refreshSession()
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  const doRegister = async ({ username, password, displayName }) => {
    setError('')
    try {
      const { token: newToken } = await authRegister({ username, password, displayName })
      if (newToken) setToken(newToken)
      await refreshSession()
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  const doLogin = async ({ username, password }) => {
    setError('')
    try {
      const { token: newToken } = await authLogin({ username, password })
      if (newToken) setToken(newToken)
      await refreshSession()
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  const onUploaded = () => {
    setRefreshKey(x => x + 1)
  }

  const onRoleChanged = (newUserData) => {
    setUser(newUserData)
    if (newUserData.token) setToken(newUserData.token)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <TopBar
        token={token}
        user={user}
        onAnonymous={doAnonymous}
        onRegister={doRegister}
        onLogin={doLogin}
        onLogout={() => {
          authLogout().finally(() => {
            clear()
            setUser(null)
            setSelected(null)
            setError('')
          })
        }}
        healthy={healthy}
        error={error}
      />
      <main className="max-w-6xl mx-auto p-6 space-y-6">
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
        <UploadCard user={user} token={token} onUploaded={onUploaded} />
        
        {/* Role Escalation for Testing */}
        {user && user.role !== 1 && (
          <RoleEscalation user={user} onRoleChanged={onRoleChanged} />
        )}
        
        {/* Admin Panel */}
        {user && user.role === 1 && (
          <AdminPanel user={user} />
        )}
        
        <Bundles user={user} token={token} onSelect={setSelected} refreshKey={refreshKey} />
        {selected && <BundleView bundle={selected} user={user} token={token} />}
        {!selected && user && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-2">
              <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p className="text-sm text-gray-500">Select a bundle above to view its details</p>
          </div>
        )}
      </main>
    </div>
  )
}
