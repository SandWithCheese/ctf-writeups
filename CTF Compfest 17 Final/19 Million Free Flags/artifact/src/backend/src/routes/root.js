  import { Router } from 'express'

  const router = Router()

  router.get('/', (req, res) => {
    res.json({
      service: 'Packrat Archivist',
      endpoints: [
        'POST /api/bundles',
        'GET /api/bundles',
        'GET /api/file/{id}/{path}',
        'GET /api/share/sign',
        'GET /api/share/export',
        'GET /api/internal/search',
        'POST /api/auth/anonymous-login',
        'POST /api/auth/register',
        'POST /api/auth/login',
      ],
      note: 'archives are extracted as-is and served back for preview',
    })
  })

  router.get('/api/health', (req, res) => {
    res.json({ ok: true })
  })

  export default router
