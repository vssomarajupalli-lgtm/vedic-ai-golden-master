# DOCKER DEPLOYMENT GUIDE
**Date:** 2026-06-18
**Phase:** 8 (Infrastructure & Deployment)

## Overview
The Vedic AI System is fully containerized using Docker and Docker Compose. This ensures zero-configuration deployment across environments while explicitly solving the WeasyPrint OS-level dependency issues required for PDF generation.

## Prerequisites
- **Docker Engine:** v20.10.0+
- **Docker Compose:** v2.0+

## Container Architecture
- **`vedic_ai_backend`**: A Python 3.11-slim container. It installs OS-level GTK dependencies (`libpango-1.0-0`, `libcairo2`, etc.) via `apt-get` to enable native WeasyPrint HTML-to-PDF rendering. Runs FastAPI via Uvicorn on port `8000`.
- **`vedic_ai_frontend`**: A multi-stage build container. Stage 1 compiles the React/Vite SPA. Stage 2 serves the static `dist` files using an Nginx Alpine container, exposed on port `3000`.

## Build and Run Instructions

### Local Development / Evaluation
To build and start the entire stack locally:
```bash
docker-compose up --build
```
Or to run in detached mode:
```bash
docker-compose up --build -d
```

### Accessing the System
- **Frontend Dashboard:** Navigate to [http://localhost:3000](http://localhost:3000)
- **Backend API Docs:** Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)

## Environment Configuration
The system is built to work out-of-the-box locally. However, if deploying to a remote server, you must pass the external domain to the frontend so it knows where to route API requests.

### Remote Deployment Example
If your backend is hosted at `https://api.vedic-ai.com`, you must pass this as a build argument when spinning up Docker Compose:

```bash
VITE_API_URL=https://api.vedic-ai.com/api/v1 docker-compose build frontend
docker-compose up -d
```

Because Vite builds a static SPA, the `VITE_API_URL` environment variable must be present *during the build step*, not just at runtime.

## Troubleshooting

### PDF Generation Still Fails
If the `ExportReport` page returns a 501 error while running in Docker:
1. Verify the backend container built successfully: `docker logs vedic_ai_backend`
2. Ensure you ran `--build` so the `apt-get install` commands fired for WeasyPrint.

### Frontend Cannot Connect to Backend
If the frontend spins endlessly on upload:
1. Open Chrome DevTools (F12) -> Network Tab.
2. Check the destination URL. If it's `http://localhost:8000/api/v1/...` and you are accessing it remotely, you forgot to set the `VITE_API_URL` during the Docker build.

## Release Packaging Strategy
For distributing releases:
1. Tag the repository: `git tag v0.8.0-dockerized`
2. Provide users with the source code or pre-built Docker images.
3. Users only need to run `docker-compose up -d` to achieve a complete, deterministic astrology engine with full PDF export capabilities.
