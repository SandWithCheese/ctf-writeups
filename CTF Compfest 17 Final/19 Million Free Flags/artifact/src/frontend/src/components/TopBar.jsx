import React, { useState } from 'react'
import { AuthModal } from './AuthModal.jsx'
import { getRoleName, getRoleColor } from '../utils/roles.js'

export function TopBar({ token, user, onAnonymous, onRegister, onLogin, onLogout, healthy, error }) {
  const [showAuthModal, setShowAuthModal] = useState(false)

  return (
    <div className="w-full border-b border-gray-200 bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="text-xl font-bold text-gray-900">Packrat Archivist</span>
          </div>
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
            healthy 
              ? 'bg-emerald-100 text-emerald-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            <div className={`w-2 h-2 rounded-full mr-1.5 ${healthy ? 'bg-emerald-500' : 'bg-red-500'}`}></div>
            {healthy ? 'Backend Online' : 'Backend Offline'}
          </span>
        </div>
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900">{user.displayName || user.username}</div>
                <div className="flex items-center gap-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getRoleColor(user.role)}`}>
                    {getRoleName(user.role)}
                  </span>
                </div>
              </div>
              {token && (
                <div className="px-2 py-1 bg-gray-100 rounded text-xs font-mono text-gray-600">
                  {token.slice(0, 8)}…
                </div>
              )}
              <button 
                className="px-4 py-2 rounded-md bg-gray-800 text-white text-sm hover:bg-gray-700 transition-colors font-medium" 
                onClick={onLogout}
              >
                Sign Out
              </button>
            </>
          ) : (
            <button 
              className="px-6 py-2 rounded-md bg-indigo-600 text-white text-sm hover:bg-indigo-700 transition-colors font-medium shadow-sm" 
              onClick={() => setShowAuthModal(true)}
            >
              Sign In
            </button>
          )}
        </div>
      </div>
      
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onLogin={onLogin}
        onRegister={onRegister}
        onAnonymous={onAnonymous}
        error={error}
      />
    </div>
  )
}
