# Samartha Vedic AI
## Golden Master Version 1.0 — Release Notes

### Major Capabilities
- **End-to-End Astrological Engine**: Comprehensive planetary strength, house strength, Ashtakavarga, Yoga detection, Vimshottari Dasha, and Gochara (Transit) calculation capabilities.
- **Dynamic Question Engine**: Hierarchical, structured astrological query parsing that routes questions to precise formula chains.
- **Explainability & Verification**: Full traceability for every calculation, ensuring transparent astrological conclusions via the newly implemented Knowledge Graph.
- **Dual Runtime Support**: Fully bundled native Desktop Application (Windows Tauri) and scalable Server Deployment (Docker/NGINX/FastAPI).
- **Client & Consultation Management**: Secure local persistence of user profiles, charts, preferences, and generated reports without data leaks.

### Architecture Summary
- **Backend**: FastAPI (Python 3.11), SQLAlchemy, PostgreSQL, Redis. Isolated `business_logic` vs `core_infrastructure`.
- **Frontend**: React 19, TypeScript, Vite, Zustand, TailwindCSS.
- **Packaging**: Tauri v2 with embedded PyInstaller Python sidecar for desktop; multi-container Docker Compose for web server.

### Engineering Achievements
- **GM-007 Determinism**: Perfect temporal propagation of `target_date_utc` across all engine layers (Transit, Dasha, QA).
- **Architecture Stabilization**: Consolidated APIs, deprecated legacy pipelines, and established a modular, data-driven Astrology Formula Calibration Framework.
- **Production QA Integrity**: Resolved critical OS-aware path resolution for Tauri PyInstaller bundles, achieving 100% test coverage and robust production persistence.

### Statistics
- **Unit & Integration Tests**: 653 Tests Passing (0 Failed)
- **Repository Health**: Clean state, strictly synchronized main branch.
- **Governance**: Fully documented Constitutional rules enforced across AI sessions.

### Supported Runtimes
- **Desktop**: Windows 10/11 x64 (MSI & NSIS installers)
- **Server**: Docker Engine (Linux/AMD64 via docker-compose)

### Known Limitations
- The `v1.0_current` calibration profile is shipped as a static JSON payload; astrology parameter tuning requires a config update.
- macOS/Linux desktop installers are not yet natively compiled.

### Future Roadmap (Version 1.1)
- **Real Horoscope Validation & Calibration**: Tuning formula constants against real-world consultation cases.
- **Cloud Account Syncing**: Remote backup for offline desktop charts.
- **Expanded Yoga Library**: Dynamic additions to planetary combination permutations.
