# API LAYER KNOWLEDGE PACKAGE

## 1. Executive Summary
The API Layer serves as the gateway between the React frontend and the Python backend. Built on FastAPI, it exposes endpoints for submitting parsed charts, executing the Question Engine, generating reports, and querying the formula registry. 

## 2. Purpose
To provide a secure, fast, and cleanly separated RESTful interface for external clients to interact with the Golden Master.

## 3. Responsibilities
- Route HTTP requests to the appropriate backend service.
- Validate request payloads using Pydantic.
- Handle exceptions and return standardized HTTP error codes.
- Manage CORS and basic security middleware.

## 4. Architecture
The API is structured using FastAPI's `APIRouter` module, centralizing endpoint registration in `router.py`.
- `/health`: System diagnostics and uptime.
- `/charts`: Endpoints for uploading and processing canonical JSON chart data.
- `/reports`: Endpoints for generating and retrieving PDFs/HTML outputs.
- `/queries`: The core entry point for the Question Engine, allowing the frontend to ask specific questions.
- `/browser`: Endpoints supporting the frontend Question Browser (fetching registries, favorites, search).

## 5. Inputs & Outputs
- **Inputs:** Standard JSON HTTP requests.
- **Outputs:** Standard JSON HTTP responses, adhering to the application's strict metadata and breakdown contract.

## 6. Implementation Files
- `backend/app/api/v1/router.py`
- `backend/app/api/v1/endpoints/health.py`
- `backend/app/api/v1/endpoints/charts.py`
- `backend/app/api/v1/endpoints/reports.py`
- `backend/app/api/v1/endpoints/queries.py`
- `backend/app/api/v1/endpoints/browser.py`

## 7. Technical Debt & Recommendations
- The API layer is currently thin, which is good. Ensure it remains purely an interface layer and does not begin to house business logic or direct mathematical calculations.
