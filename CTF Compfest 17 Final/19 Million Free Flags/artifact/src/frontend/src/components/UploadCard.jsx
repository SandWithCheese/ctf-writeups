import React, { useState } from 'react'

import { uploadBundle } from '../api.js'

export function UploadCard({ user, token, onUploaded }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [file, setFile] = useState(null)

  const canUpload = !!user && !!file && !busy

  const doUpload = async () => {
    if (!file) return
    setBusy(true)
    setError('')
    try {
      await uploadBundle(file, token)
      setFile(null)
      onUploaded?.()
    } catch (e) {
      setError(String(e.message || e))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="p-6 border border-gray-200 rounded-lg bg-white shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Upload Archive</h3>
        {user && (
          <span className="text-sm text-green-600 bg-green-50 px-2 py-1 rounded-full">
            ✓ Authenticated
          </span>
        )}
      </div>
      
      <div className="space-y-4">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Choose Archive File
            </label>
            <input
              type="file"
              accept=".tar,.tar.gz,.tgz"
              onChange={e => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            {file && (
              <p className="mt-2 text-sm text-gray-600">
                Selected: <span className="font-mono">{file.name}</span>
                <span className="ml-2 text-gray-500">
                  ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </span>
              </p>
            )}
          </div>
          <div className="flex-shrink-0">
            <button
              className={`px-6 py-3 rounded-md text-sm font-medium transition-colors ${
                canUpload 
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2' 
                  : 'bg-gray-200 text-gray-500 cursor-not-allowed'
              }`}
              disabled={!canUpload}
              onClick={doUpload}
            >
              {busy ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Uploading...
                </span>
              ) : (
                'Upload Archive'
              )}
            </button>
          </div>
        </div>
        
        <div className="text-sm text-gray-500 bg-gray-50 p-3 rounded-md">
          <p><strong>Requirements:</strong></p>
          <ul className="mt-1 space-y-1">
            <li>• Maximum file size: 2 MB</li>
            <li>• Supported formats: .tar, .tar.gz, .tgz</li>
            <li>• Must be logged in to upload</li>
          </ul>
        </div>
        
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}
