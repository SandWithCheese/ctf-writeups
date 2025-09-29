import crypto from 'crypto'
import fs from 'fs/promises'

export const UPLOAD_ROOT = process.env.UPLOAD_ROOT || '/srv/uploads'
export const MAX_ARCHIVE_SIZE = Number.parseInt(process.env.MAX_ARCHIVE_SIZE || String(2 * 1024 * 1024), 10)
export const SHARE_SECRET = crypto.randomBytes(32)

export async function ensureUploadRoot() {
  await fs.mkdir(UPLOAD_ROOT, { recursive: true }).catch(() => {})
}

