import React, { useEffect, useMemo, useState } from 'react'

import { buildShareUrl, fetchFileBlob } from '../api.js'

export function BundleView({ bundle, user, token }) {
  const [shareBusy, setShareBusy] = useState('')
  const [downloadBusy, setDownloadBusy] = useState(false)
  const [downloadError, setDownloadError] = useState('')
  const [downloadUrl, setDownloadUrl] = useState('')
  const [fileForShare, setFileForShare] = useState('')
  const [minutes, setMinutes] = useState(15)

  useEffect(() => () => {
    if (downloadUrl) {
      URL.revokeObjectURL(downloadUrl)
    }
  }, [downloadUrl])

  const expEpoch = useMemo(
    () => Math.floor(Date.now() / 1000) + (parseInt(minutes || 0, 10) * 60),
    [minutes]
  )

  const onSelectFile = file => {
    if (downloadUrl) {
      URL.revokeObjectURL(downloadUrl)
      setDownloadUrl('')
    }
    setFileForShare(file)
    setDownloadError('')
    setShareBusy('')
  }

  const createShare = async () => {
    if (!fileForShare) return
    setShareBusy('Building link…')
    try {
      const url = await buildShareUrl({ id: bundle.id, path: fileForShare, expEpoch })
      window.open(url, '_blank')
      setShareBusy('Opened in new tab.')
      setTimeout(() => setShareBusy(''), 1500)
    } catch (e) {
      setShareBusy(String(e.message || e))
    }
  }

  const downloadSelected = async () => {
    if (!fileForShare) return
    setDownloadBusy(true)
    setDownloadError('')
    if (downloadUrl) {
      URL.revokeObjectURL(downloadUrl)
      setDownloadUrl('')
    }
    try {
      const { blob } = await fetchFileBlob(bundle.id, fileForShare, token)
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
      const link = document.createElement('a')
      link.href = url
      const namePart = fileForShare.split('/').pop() || fileForShare
      link.download = namePart
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (e) {
      setDownloadError(String(e.message || e))
    } finally {
      setDownloadBusy(false)
    }
  }

  return (
    <div className="p-6 border border-gray-200 rounded-lg bg-white shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Bundle Details</h3>
          <p className="text-sm text-gray-500 font-mono">{bundle.id}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            {bundle.files.length} files
          </span>
          <button
            onClick={() => window.history.back()}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      <div className="space-y-6">
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">Files</h4>
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <div className="max-h-80 overflow-auto">
              {bundle.files.map(file => (
                <div key={file} className={`px-3 py-2 text-sm flex items-center justify-between border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors ${fileForShare === file ? 'bg-indigo-50 border-indigo-200' : ''}`}>
                  <span className="truncate font-mono text-gray-900" title={file}>{file}</span>
                  <button
                    className={`ml-2 px-3 py-1 text-xs rounded-md font-medium transition-colors ${
                      fileForShare === file 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-emerald-600 text-white hover:bg-emerald-700'
                    }`}
                    onClick={() => onSelectFile(file)}
                  >
                    {fileForShare === file ? 'Selected' : 'Select'}
                  </button>
                </div>
              ))}
              {bundle.files.length === 0 && (
                <div className="px-3 py-4 text-sm text-gray-500 text-center">No files found.</div>
              )}
            </div>
          </div>
        </div>
        
        <div className="p-4 border border-gray-200 rounded-lg bg-gray-50">
          <div className="text-sm font-medium text-gray-700 mb-3">
            Selected File: <span className="font-mono text-gray-900">{fileForShare || 'None'}</span>
          </div>
          
          {fileForShare && (
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <label className="text-sm font-medium text-gray-700">Share expires in:</label>
                <input
                  type="number"
                  min="1"
                  value={minutes}
                  onChange={e => setMinutes(e.target.value)}
                  className="w-20 px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
                <span className="text-sm text-gray-600">minutes</span>
              </div>
              
              <div className="flex items-center gap-3">
                <button
                  className={`px-4 py-2 text-sm rounded-md font-medium transition-colors ${
                    !downloadBusy 
                      ? 'bg-gray-800 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2' 
                      : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                  }`}
                  disabled={!fileForShare || downloadBusy}
                  onClick={downloadSelected}
                >
                  {downloadBusy ? (
                    <span className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Downloading...
                    </span>
                  ) : (
                    'Download File'
                  )}
                </button>
                
                <button
                  className={`px-4 py-2 text-sm rounded-md font-medium transition-colors ${
                    fileForShare 
                      ? 'bg-emerald-600 text-white hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2' 
                      : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                  }`}
                  disabled={!fileForShare}
                  onClick={createShare}
                >
                  Create Share Link
                </button>
              </div>
              
              {shareBusy && (
                <div className="p-2 bg-blue-50 border border-blue-200 rounded-md">
                  <p className="text-xs text-blue-600">{shareBusy}</p>
                </div>
              )}
              {downloadError && (
                <div className="p-2 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-xs text-red-600">{downloadError}</p>
                </div>
              )}
            </div>
          )}
          
          {!fileForShare && (
            <p className="text-sm text-gray-500">Select a file above to download or share it</p>
          )}
        </div>
      </div>
    </div>
  )
}
