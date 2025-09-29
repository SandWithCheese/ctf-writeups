import { Router } from 'express'
import fs from 'fs/promises'
import path from 'path'

import { UPLOAD_ROOT } from '../config.js'
import { requireAuth } from '../middleware/auth.js'
import { sendError } from '../utils.js'

const MAX_RESULTS = 200

const router = Router()

router.get('/internal/search', requireAuth, async (req, res) => {
  if (!req.user || req.user.role !== 1) {
    return sendError(res, 403, 'insufficient privileges')
  }

  const keyword = String(req.query.keyword || '')

  const matches = []

  try {
    const entries = await fs.readdir(UPLOAD_ROOT, { withFileTypes: true })
    
    for (const bundleDir of entries) {
      if (!bundleDir.isDirectory() || matches.length >= MAX_RESULTS) continue
      
      if (!keyword || bundleDir.name.toLowerCase().includes(keyword.toLowerCase())) {
        matches.push({
          type: 'bundle',
          id: bundleDir.name,
          name: bundleDir.name,
          match: keyword ? `Found bundle matching "${keyword}"` : 'All bundles'
        })
      }
    }
  } catch (error) {
    console.error('Search error:', error)
    return sendError(res, 500, 'search failed')
  }

  res.json({ keyword, totalMatches: matches.length, matches })
})

router.get('/internal/bundle/:bundleId/files', requireAuth, async (req, res) => {
  if (!req.user || req.user.role !== 1) {
    return sendError(res, 403, 'insufficient privileges')
  }

  const { bundleId } = req.params
  if (!bundleId) {
    return sendError(res, 400, 'bundle ID required')
  }

  const bundlePath = path.join(UPLOAD_ROOT, decodeURIComponent(bundleId))
  
  try {
    const entries = await fs.readdir(bundlePath, { withFileTypes: true })
    const files = []
    
    for (const entry of entries) {
      if (entry.isFile()) {
        try {
          const filePath = path.join(bundlePath, entry.name)
          const stats = await fs.stat(filePath)
          files.push({
            name: entry.name,
            size: stats.size,
            modified: stats.mtime.toISOString()
          })
        } catch {
          files.push({
            name: entry.name,
            size: 0,
            modified: null,
            error: 'Unable to read file stats'
          })
        }
      } else if (entry.isDirectory()) {
        files.push({
          name: entry.name + '/',
          type: 'directory'
        })
      }
    }
    
    res.json({ bundleId, files })
  } catch (error) {
    console.error('Bundle list error:', error)
    return sendError(res, error.code === 'ENOENT' ? 404 : 500, 'failed to list bundle contents')
  }
})

router.get('/internal/bundle/:bundleId/download/*', requireAuth, async (req, res) => {
  if (!req.user || req.user.role !== 1) {
    return sendError(res, 403, 'insufficient privileges')
  }

  const { bundleId } = req.params
  const filePath = req.params[0] || ''
  
  if (!bundleId) {
    return sendError(res, 400, 'bundle ID required')
  }
  if (!filePath) {
    return sendError(res, 400, 'file path required')
  }

  const targetPath = path.join(UPLOAD_ROOT, decodeURIComponent(bundleId), filePath)
  
  try {
    await fs.stat(targetPath)
    return res.download(targetPath, req.query.saveAs || path.basename(filePath), (err) => {
      if (err && !res.headersSent) {
        console.error('Download interrupted:', err)
        return sendError(res, err.code === 'ENOENT' ? 404 : 500, err.message || 'download failed')
      }
    })
  } catch (error) {
    console.error('Download error:', error)
    return sendError(res, error.code === 'ENOENT' ? 404 : 500, error.message || 'download failed')
  }
})

export default router

