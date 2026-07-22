# Samartha Vedic AI
## Golden Master Version 1.0 Handover
**STARTUP DOCUMENT FOR ALL FUTURE AI SESSIONS**

### 1. Project Overview & Current Version
**Project:** Samartha Vedic AI
**Version:** Golden Master 1.0 (Feature Frozen)
**Description:** A professional-grade, mathematically rigorous Vedic Astrology application featuring a deterministic formula engine, a hierarchical question parser, and full explainability via a transparent Knowledge Graph. It operates as both a standalone Windows Desktop Application and a scalable Web Server.

### 2. Repository & Architecture Overview
**Repository Status:** CLEAN. `main` is the frozen source of truth.
**Architecture:**
- **Backend:** FastAPI (Python), PostgreSQL, Redis.
- **Frontend:** React, TypeScript, Zustand, TailwindCSS, Vite.
- **Packaging:** Tauri v2 for Desktop (embedding a PyInstaller-bundled Python backend sidecar), and Docker Compose for Server deployment.

### 3. Engineering Principles & Frozen Governance
- **Repository First:** The code is the ultimate source of truth, superseding conversational history.
- **Evidence Before Conclusions:** All architectural conclusions must be backed by verifiable repository evidence (grep, ls, etc.).
- **Parameter-Driven Evolution:** Core astrology business logic is strictly frozen. All astrological formula changes or calibrations must be performed via parameter updates in configuration files (e.g., JSON/SQLite payloads), NOT by rewriting Python code.
- **Temporal Determinism:** All operations must respect `target_date_utc` linearly without implicit time dependencies.

### 4. Repository Structure
- `backend/`: FastAPI application, astrology engines, deterministic logic.
- `frontend/`: React Vite application.
- `frontend/src-tauri/`: Tauri packaging and PyInstaller sidecar hook.
- `docs/`: Governance, ADRs, status tracking, release notes.
- `docker-compose.yml`: Server deployment configuration.

### 5. Current Project Status & Major Milestones Completed
- **Status:** **GOLDEN MASTER 1.0 CLOSED**.
- **Completed Milestones:**
  - GM-005/006: Temporal Engine and Question Engine integration.
  - GM-007: Determinism finalization.
  - GM-008: End-to-End Product completion.
  - GM-009: Release Candidate Build.
  - GM-010: Production QA (Desktop & Docker) and Feature Freeze.
  - GM-011/012: Version 1.0 Project Closure.

### 6. Validation Workflow
1. **Analyze:** Verify existing code before making any edits.
2. **Review:** Cross-reference existing ADRs and Governance rules.
3. **Execute:** Implement deterministic, localized changes.
4. **Test:** Run Python tests (`pytest`), `cargo check`, and verify `git status`.

### 7. AI Assistant Guidelines
**What you MAY do:**
- Explore the repository to answer analytical queries.
- Build upon Version 1.1 roadmap items ONLY if explicitly instructed by the user.
- Read ADRs (`docs/architecture/decisions/`) and Governance documents (`docs/governance/`) to maintain context.

**What you MUST NEVER do:**
- NEVER modify Golden Master Version 1.0 core business logic or astrological calculation engines.
- NEVER introduce temporary fixes or unstructured code overrides.
- NEVER bypass the Parameter-Driven Evolution rule for astrological feedback.
- NEVER create new engineering backlogs without explicit architectural approval.

### 8. Future Roadmap (Version 1.1)
- **GM-011 (Next Phase):** Real Horoscope Validation & Calibration (adjusting config weights).
- **Cloud Integrations:** Optional remote syncing of local charts.

### 9. Session Startup Instructions
**For the AI Agent:**
1. Acknowledge this document.
2. Assume the system is fully functional and frozen at Version 1.0.
3. Verify repository state using `git status`.
4. Wait for the user's specific operational instruction before modifying any files.
5. If asked to fix an astrological calculation, strictly look for calibration files or constants to update, rather than modifying the core Engine logic.
