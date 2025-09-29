import express from 'express'
import cookieParser from 'cookie-parser'
import multer from 'multer'

import { ensureUploadRoot } from './config.js'
import rootRouter from './routes/root.js'
import authRouter from './routes/auth.js'
import createBundlesRouter from './routes/bundles.js'
import filesRouter from './routes/files.js'
import shareRouter from './routes/share.js'
import internalRouter from './routes/internal.js'

await ensureUploadRoot()

const app = express()
app.disable('x-powered-by')
app.use(cookieParser())
app.use(express.json())

app.use((req, res, next) => {
  const start = process.hrtime.bigint()
  res.on('finish', () => {
    const durMs = Number(process.hrtime.bigint() - start) / 1e6
    const len = res.get('content-length') || '-'
    console.log(`[req] ${req.ip} ${req.method} ${req.originalUrl} -> ${res.statusCode} ${len} ${durMs.toFixed(1)}ms`)
  })
  next()
})

const upload = multer({ storage: multer.memoryStorage() })

app.use('/', rootRouter)
app.use('/api/auth', authRouter)
app.use('/api', createBundlesRouter(upload))
app.use('/api', filesRouter)
app.use('/api', shareRouter)
app.use('/api', internalRouter)

const host = process.env.HOST || '0.0.0.0'
const port = Number.parseInt(process.env.PORT || process.env.UVICORN_PORT || '5000', 10)
app.listen(port, host, () => {
  console.log(`[backend] listening on ${host}:${port}`)
})
