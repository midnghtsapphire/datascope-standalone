# Deployment Guide

This guide covers a production-oriented deployment path for DataScope Standalone with:
- Python backend services
- React dashboard build pipeline
- Website in Test hosted on Vercel

## 1) Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+ (for root baseline scripts)
- Corepack (to provision pnpm for frontend build steps)
- Docker (optional)

## 2) Local validation

```bash
npm test
npm run build
```

If frontend dependencies are needed:

```bash
cd cybersecurity-threat-dashboard
corepack enable
pnpm install --frozen-lockfile
pnpm build
```

## 3) Environment setup

1. Copy `.env.example` to `.env`.
2. Set production values for:
   - API keys
   - database/cache connection strings
   - security-sensitive tokens

Never commit `.env` files.

## 4) Backend deployment

### Option A — Docker Compose

```bash
docker compose up --build -d
```

### Option B — Python process

```bash
pip install -r requirements.txt
python enhanced_main.py
```

## 5) Frontend deployment (Website in Test)

- Target test URL: `https://datascope-standalone.vercel.app`
- Deploy using Vercel Git integration from this repository.

## 6) Deployment automation reference

- Baseline checks are codified in:
  - `scripts/test-baseline.js`
  - `scripts/build-baseline.js`
- Run these checks in CI prior to production promotion.
