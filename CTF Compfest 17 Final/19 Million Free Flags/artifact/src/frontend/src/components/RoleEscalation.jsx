import React, { useState } from 'react'
import { escalateRole } from '../api.js'

export function RoleEscalation({ user, onRoleChanged }) {
  const [secret, setSecret] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleEscalate = async (e) => {
    e.preventDefault()
    if (!secret.trim()) return

    setLoading(true)
    setError('')
    setSuccess('')
    
    try {
      const result = await escalateRole(secret)
      setSuccess(result.message || 'Role escalated successfully!')
      setSecret('')
      onRoleChanged?.(result)
    } catch (e) {
      setError(String(e.message || e))
    } finally {
      setLoading(false)
    }
  }

  if (user && user.role === 1) {
    return (
      <div className="p-4 border border-green-200 rounded-lg bg-green-50">
        <div className="flex items-center">
          <svg className="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-sm text-green-800">You already have administrator privileges!</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 border border-gray-200 rounded-lg bg-white">
      <h4 className="text-sm font-medium text-gray-900 mb-3">Role Escalation (Testing Only)</h4>
      <form onSubmit={handleEscalate} className="space-y-3">
        <div>
          <label htmlFor="secret" className="block text-xs font-medium text-gray-700 mb-1">
            Escalation Key
          </label>
          <input
            type="text"
            id="secret"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            placeholder="Enter escalation key..."
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !secret.trim()}
          className="w-full px-3 py-2 text-sm bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Escalating...' : 'Escalate to Admin'}
        </button>
      </form>
      
      {error && (
        <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded-md">
          <p className="text-xs text-red-600">{error}</p>
        </div>
      )}
      
      {success && (
        <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded-md">
          <p className="text-xs text-green-600">{success}</p>
        </div>
      )}
    </div>
  )
}
