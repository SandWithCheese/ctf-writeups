import { Router } from 'express'
import fs from 'fs/promises'
import path from 'path'

import { UPLOAD_ROOT } from '../config.js'
import { requireAuth } from '../middleware/auth.js'
import { bundleOwnership, sendError } from '../utils.js'

const router = Router()

router.get('/file/:bid/*', requireAuth, async (req, res) => {
  const { bid } = req.params
  const relPath = req.params[0] || ''
  const access = bundleOwnership(req.user, bid)
  if (access.error) return sendError(res, access.error.status, access.error.detail)
  const isSafePath = (name) => typeof name === 'string' && name && /^[\w\-. ]+$/.test(name) && !name.includes('..')
  if (!isSafePath(relPath)) {
    return sendError(res, 400, 'invalid path')
  }
  try {
    const bundleDir = path.join(UPLOAD_ROOT, bid)
    process.chdir(bundleDir)
    return res.download(relPath, req.query.saveAs || relPath, (err) => {
      if (err && !res.headersSent) {
        console.error('Download interrupted:', err);
        return sendError(res, err.code === 'ENOENT' ? 404 : 500, err.message || 'download failed')
      }
    })
  } catch (error) {
    console.error('Download error:', error);
    return sendError(res, error.code === 'ENOENT' ? 404 : 500, error.message || 'download failed')
  }
})

export default router
