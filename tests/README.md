# Repository Tests

This directory provides the repository-level test entry point per Documentation Constitution 4.2.

## Test Organization

- **Backend Tests**: `../backend/tests/` - Python pytest suite for all deterministic engines
- **Frontend Tests**: `../frontend/` - Vitest/Jest suite for UI components

## Running Tests

```bash
# Backend tests
cd backend && python -m pytest tests/

# Frontend tests
cd frontend && npm test
```

All tests are organized under their respective application directories.
