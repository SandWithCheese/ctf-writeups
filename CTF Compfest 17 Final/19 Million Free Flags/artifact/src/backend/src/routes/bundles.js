import { Router } from "express"
import crypto from "crypto"
import fs from "fs/promises"
import path from "path"
import tar from "tar"

import { MAX_ARCHIVE_SIZE, UPLOAD_ROOT } from "../config.js"
import { ensureUserBundles, INDEX } from "../state.js"
import { requireAuth } from "../middleware/auth.js"
import { listFiles, sendError } from "../utils.js"

async function validateTarNoLinks(tmpPath) {
  const invalid = []
  await tar.t({
    file: tmpPath,
    onentry: (entry) => {
      if (entry.type === "SymbolicLink" || entry.type === "Link") {
        invalid.push(`link not allowed: ${entry.path}`)
      }
      if (path.isAbsolute(entry.path) || entry.path.startsWith("/")) {
        invalid.push(`absolute path not allowed: ${entry.path}`)
      }
      const normalized = path.posix.normalize("/" + entry.path)
      if (normalized.includes("/..")) {
        invalid.push(`path traversal not allowed: ${entry.path}`)
      }
    },
  })
  if (invalid.length) throw new Error(invalid.join("; "))
}

function createBundlesRouter(upload) {
  const router = Router()

  router.post(
    "/bundles",
    requireAuth,
    upload.single("archive"),
    async (req, res) => {
      try {
        if (!req.file || !req.file.buffer)
          return sendError(res, 400, "missing archive")
        const blob = req.file.buffer
        if (blob.length > MAX_ARCHIVE_SIZE)
          return sendError(res, 400, "archive too large")
        const bid = crypto.randomBytes(6).toString("hex")
        const dest = path.join(UPLOAD_ROOT, bid)
        await fs.mkdir(dest, { recursive: true })
        try {
          const tmpPath = path.join(dest, ".upload.tmp")
          await fs.writeFile(tmpPath, blob)
          await validateTarNoLinks(tmpPath) // Validate the tar file to prevent symlink attacks
          await tar.x({
            file: tmpPath,
            cwd: dest,
            strict: false,
            noChmod: true,
            noMtime: true,
          })
          await fs.unlink(tmpPath).catch(() => {})
        } catch (error) {
          return sendError(res, 400, `invalid tar: ${error.message || error}`)
        }
        const files = await listFiles(dest)
        const info = { id: bid, files, created_at: Date.now() / 1000 }
        INDEX.set(bid, info)
        ensureUserBundles(req.user.userId).add(bid)
        return res.json(info)
      } catch (error) {
        console.error("[error] /api/bundles", error)
        return sendError(res, 500, "internal error")
      }
    }
  )

  router.get("/bundles", requireAuth, (req, res) => {
    const ids = Array.from(ensureUserBundles(req.user.userId))
    const items = ids
      .filter((id) => INDEX.has(id))
      .sort()
      .map((id) => INDEX.get(id))
    res.json(items)
  })

  return router
}

export default createBundlesRouter
