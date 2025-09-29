import React, { useState, useEffect } from 'react'
import { searchBundles, getBundleFiles, downloadInternalFile } from '../api.js'

export function AdminPanel({ user }) {
  const [searchKeyword, setSearchKeyword] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [selectedBundle, setSelectedBundle] = useState(null)
  const [bundleFiles, setBundleFiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('search')

  const performSearch = async () => {
    if (!user || user.role !== 1) return
    
    setLoading(true)
    setError('')
    try {
      const results = await searchBundles(searchKeyword)
      setSearchResults(results.matches || [])
    } catch (e) {
      setError(String(e.message || e))
    } finally {
      setLoading(false)
    }
  }

  const loadBundleFiles = async (bundleId) => {
    if (!user || user.role !== 1) return
    
    setLoading(true)
    setError('')
    try {
      const result = await getBundleFiles(bundleId)
      setBundleFiles(result.files || [])
      setSelectedBundle(bundleId)
      setActiveTab('files')
    } catch (e) {
      setError(String(e.message || e))
    } finally {
      setLoading(false)
    }
  }

  const downloadFile = async (bundleId, filePath, fileName) => {
    if (!user || user.role !== 1) return
    
    try {
      const { blob } = await downloadInternalFile(bundleId, filePath, fileName)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = fileName || filePath.split('/').pop()
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
    } catch (e) {
      setError(String(e.message || e))
    }
  }

  useEffect(() => {
    if (user && user.role === 1) {
      performSearch()
    }
  }, [user])

  if (!user || user.role !== 1) {
    return (
      <div className="p-6 border border-gray-200 rounded-lg bg-white shadow-sm">
        <div className="text-center py-8">
          <div className="text-gray-400 mb-2">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <p className="text-sm text-gray-500">Administrator access required</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 border border-gray-200 rounded-lg bg-white shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Administrator Panel</h3>
          <p className="text-sm text-gray-500">System-wide bundle management and search</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
            Admin Access
          </span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('search')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'search'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Bundle Search
          </button>
          {selectedBundle && (
            <button
              onClick={() => setActiveTab('files')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'files'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Bundle Files
            </button>
          )}
        </nav>
      </div>

      {/* Search Tab */}
      {activeTab === 'search' && (
        <div className="space-y-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              placeholder="Search bundles by ID..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && performSearch()}
            />
            <button
              onClick={performSearch}
              disabled={loading}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>

          <div className="space-y-2">
            {searchResults.map((result) => (
              <div key={result.id} className="p-3 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-mono text-sm font-medium text-gray-900">{result.id}</div>
                    <div className="text-xs text-gray-500">{result.match}</div>
                  </div>
                  <button
                    onClick={() => loadBundleFiles(result.id)}
                    className="px-3 py-1 text-xs bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
                  >
                    View Files
                  </button>
                </div>
              </div>
            ))}
            {searchResults.length === 0 && !loading && (
              <div className="text-center py-4 text-sm text-gray-500">
                {searchKeyword ? 'No bundles found matching your search' : 'No bundles found'}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Files Tab */}
      {activeTab === 'files' && selectedBundle && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-gray-900">Bundle: {selectedBundle}</h4>
              <p className="text-xs text-gray-500">{bundleFiles.length} files</p>
            </div>
            <button
              onClick={() => setActiveTab('search')}
              className="px-3 py-1 text-xs bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
            >
              Back to Search
            </button>
          </div>

          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <div className="max-h-80 overflow-auto">
              {bundleFiles.map((file, index) => (
                <div key={index} className="px-3 py-2 border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="font-mono text-sm text-gray-900">{file.name}</div>
                      {file.size !== undefined && (
                        <div className="text-xs text-gray-500">
                          {file.type === 'directory' ? 'Directory' : `${(file.size / 1024).toFixed(1)} KB`}
                          {file.modified && ` • Modified: ${new Date(file.modified).toLocaleString()}`}
                        </div>
                      )}
                      {file.error && (
                        <div className="text-xs text-red-500">{file.error}</div>
                      )}
                    </div>
                    {file.type !== 'directory' && (
                      <button
                        onClick={() => downloadFile(selectedBundle, file.name, file.name)}
                        className="ml-2 px-2 py-1 text-xs bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors"
                      >
                        Download
                      </button>
                    )}
                  </div>
                </div>
              ))}
              {bundleFiles.length === 0 && (
                <div className="px-3 py-4 text-sm text-gray-500 text-center">No files found</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
