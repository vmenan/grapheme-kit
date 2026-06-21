# graphemes++ demo site

A small, paper-grade demo website for the `graphemes_plusplus` library. Every
number shown is produced by the **real library** (and `sacrebleu`) running in a
Python backend — nothing is reimplemented in JavaScript.

```
demo/
  backend/   FastAPI service that imports graphemes_plusplus unchanged
  frontend/  Next.js (static export) UI, deploys to Cloudflare Pages
```

Two tools, matching the meeting brief:

- **Metrics** (`/metrics`) — paste a reference + prediction *or* upload two
  line-aligned files. Shows grapheme-level **chrF / chrF++** next to the standard
  code-point baselines, plus **CER** and **Levenshtein** (each shown at both the
  grapheme and code-point level), with a dropdown to focus one metric family.
- **Decomposition** (`/decompose`) — segment text into grapheme clusters and
  decompose Tamil/Sinhala into phonetic units, with a recompose round-trip check.

---

## Architecture

```
Browser (Cloudflare Pages, static)
   |  fetch JSON  (NEXT_PUBLIC_API_BASE_URL)
   v
FastAPI  ->  import graphemes_plusplus   (real sacrebleu, Python 3.14)
```

The frontend is fully static, so it can live on Cloudflare Pages; the backend is
a portable Docker image you can host anywhere that binds `$PORT`.

---

## Run locally

### Option A — Docker (one command)

```bash
cd demo
docker compose up --build
# UI:  http://localhost:3000
# API: http://localhost:7860/api/health
```

### Option B — run each part directly

**Backend** (needs Python 3.14; `uv` will fetch it):

```bash
cd demo/backend
uv venv --python 3.14 .venv
uv pip install --python .venv -e ../.. -r requirements.txt
./.venv/Scripts/python -m uvicorn app.main:app --reload --port 7860   # Windows
# source .venv/bin/activate && uvicorn app.main:app --reload --port 7860   # macOS/Linux
```

**Frontend:**

```bash
cd demo/frontend
cp .env.example .env.local      # points at http://localhost:7860
npm install
npm run dev                     # http://localhost:3000
```

### Tests

```bash
# Library tests (unchanged):
cd graphemes_plusplus && pytest

# Backend parity tests (API reproduces library numbers):
cd demo/backend && ./.venv/Scripts/python -m pytest tests -q
```

---

## Deploy

### Backend — Docker, host-agnostic

The same image runs on Hugging Face Spaces, Koyeb, or your own instance; it binds
`0.0.0.0:$PORT` (default `7860`).

```bash
# from the repo root (context must be the repo root):
docker build -f demo/backend/Dockerfile -t graphemes-demo-api .
docker run -p 7860:7860 graphemes-demo-api
```

- **Hugging Face Spaces (Docker):** create a Docker Space, add this `Dockerfile`
  (it already exposes 7860). Set `GRAPHEMES_CORS_ORIGINS` to your Pages URL.
- **Koyeb:** deploy from the Dockerfile; Koyeb injects `$PORT` automatically.
- **Your instance:** `docker run -e PORT=7860 -p 7860:7860 ...`.

Set `GRAPHEMES_CORS_ORIGINS` (comma-separated) to the frontend origin(s) in
production instead of the default `*`.

### Frontend — Cloudflare Pages

```bash
cd demo/frontend
NEXT_PUBLIC_API_BASE_URL="https://<your-backend-url>" npm run build
# outputs ./out  — upload as a static site
```

Cloudflare Pages settings:

- Build command: `npm run build`
- Build output directory: `out`
- Environment variable: `NEXT_PUBLIC_API_BASE_URL = https://<your-backend-url>`

---

## Environment variables

| Variable | Where | Purpose |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | frontend (build time) | Base URL of the backend API |
| `PORT` | backend | Port to bind (default `7860`) |
| `GRAPHEMES_CORS_ORIGINS` | backend | Comma-separated allowed origins (default `*`) |
