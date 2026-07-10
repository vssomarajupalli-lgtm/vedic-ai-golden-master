# PROJECT_REQUIREMENTS.md

## Version 1 Capabilities (COMPLETED)
1. Ingest `canonical_content.json` and `machine_index.json`.
2. Calculate dignity, strength, and house impacts for all 9 planets.
3. Calculate Vimshottari Dasha periods and live transits (Gochara).
4. Detect Parashari Yogas dynamically.
5. Provide a Master Probability Grade for 8 life domains.
6. Provide a web dashboard (PWA) to upload data and visualize results instantly.
7. Allow natural language querying grounded in the mathematical output.
8. Generate downloadable HTML, PDF, and JSON reports.

## Version 2 Capabilities (UPCOMING)
1. **Authentication**: User accounts, JWTs, secure login.
2. **Persistence**: PostgreSQL database via SQLAlchemy to store user profiles and historical chart data.
3. **Advanced Math**: Complete internal Shadbala calculation engine to replace dependency on PDF-extracted values.
4. **DevOps**: Docker containers for the FastAPI backend (with compiled C-libraries for `swisseph`) and static NGINX serving for the frontend. 

## Non-Functional Requirements
- Maintain 100% test passing rate on all Pull Requests.
- Keep the `PipelineRunner` strictly stateless and uncoupled from database IO.
- Ensure the React PWA achieves a Lighthouse score of 95+ for accessibility and performance.
