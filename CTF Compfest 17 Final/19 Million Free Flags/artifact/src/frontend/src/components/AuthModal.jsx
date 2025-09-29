import React, { useState } from 'react'

export function AuthModal({ isOpen, onClose, onLogin, onRegister, onAnonymous, error }) {
  const [mode, setMode] = useState('login') // 'login', 'register', 'anonymous'
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    displayName: ''
  })
  const [loading, setLoading] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      if (mode === 'login') {
        await onLogin({ username: formData.username, password: formData.password })
      } else if (mode === 'register') {
        await onRegister({ 
          username: formData.username, 
          password: formData.password, 
          displayName: formData.displayName || formData.username 
        })
      } else if (mode === 'anonymous') {
        await onAnonymous()
      }
      onClose()
    } catch (e) {
      // Error handling is done in parent component
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setFormData({ username: '', password: '', displayName: '' })
  }

  const switchMode = (newMode) => {
    setMode(newMode)
    resetForm()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {mode === 'login' && 'Sign In'}
              {mode === 'register' && 'Create Account'}
              {mode === 'anonymous' && 'Anonymous Access'}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          {mode === 'anonymous' ? (
            <div className="space-y-4">
              <p className="text-gray-600 text-sm">
                Get started quickly with anonymous access. You can always create an account later.
              </p>
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Signing in...' : 'Continue Anonymously'}
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                  Username
                </label>
                <input
                  type="text"
                  id="username"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter your username"
                  required
                  minLength={3}
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter your password"
                  required
                  minLength={4}
                />
              </div>

              {mode === 'register' && (
                <div>
                  <label htmlFor="displayName" className="block text-sm font-medium text-gray-700 mb-1">
                    Display Name (optional)
                  </label>
                  <input
                    type="text"
                    id="displayName"
                    value={formData.displayName}
                    onChange={(e) => setFormData({ ...formData, displayName: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    placeholder="How should we display your name?"
                    maxLength={48}
                  />
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Please wait...' : (mode === 'login' ? 'Sign In' : 'Create Account')}
              </button>
            </form>
          )}

          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="flex flex-col space-y-2">
              {mode !== 'login' && (
                <button
                  onClick={() => switchMode('login')}
                  className="text-sm text-indigo-600 hover:text-indigo-500 transition-colors"
                >
                  Already have an account? Sign in
                </button>
              )}
              {mode !== 'register' && (
                <button
                  onClick={() => switchMode('register')}
                  className="text-sm text-indigo-600 hover:text-indigo-500 transition-colors"
                >
                  Need an account? Create one
                </button>
              )}
              {mode !== 'anonymous' && (
                <button
                  onClick={() => switchMode('anonymous')}
                  className="text-sm text-gray-600 hover:text-gray-500 transition-colors"
                >
                  Just browsing? Continue anonymously
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
