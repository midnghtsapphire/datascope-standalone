# Deployment Guide

## Deployment Targets
- **Website in test (Vercel):** deploy `cybersecurity-threat-dashboard/` as the frontend surface.
- **Backend/API (Docker):** deploy root Flask service via Docker/Gunicorn.

## 1) Local Production Validation
```bash
npm test
npm run build
docker compose build datascope
docker compose up -d datascope
```

Verify status:
```bash
curl -f http://localhost:5000/api/status
```

## 2) Frontend Deploy (Vercel)
Deploy the dashboard directory:
```bash
cd cybersecurity-threat-dashboard
npm install --legacy-peer-deps
npm run build
```

Then deploy with Vercel CLI or Vercel Git integration.

## 3) Backend Deploy (Container)
```bash
docker compose build datascope
docker compose up -d datascope
```

Required environment variables:
- `SECRET_KEY`
- `DATABASE_URL`
- `LOG_LEVEL`
- `VITE_API_BASE_URL` (frontend build/runtime)

## 4) Post-Deploy Checklist
- API health endpoint returns 200
- Frontend loads and calls backend successfully
- Reports can be generated to `reports/`
- Security headers and secret values verified
