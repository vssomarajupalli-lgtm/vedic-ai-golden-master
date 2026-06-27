# DEPENDENCY AUDIT REPORT
**Date:** 2026-06-18
**Context:** Phase 8 WeasyPrint Runtime Failure

## The Issue
During runtime inside the Docker container, WeasyPrint successfully imports but crashes during the `write_pdf()` execution with:
`AttributeError: 'super' object has no attribute 'transform'`

## The Root Cause
A thorough dependency audit reveals the exact source of this error:
1. `backend/requirements.txt` strictly pins `weasyprint==62.1`.
2. `weasyprint` inherently relies on a secondary package called `pydyf` to construct the actual PDF binary stream.
3. `pydyf` is **not pinned** in `requirements.txt`.
4. When `docker-compose build` executes `pip install -r requirements.txt`, it pulls the exact `weasyprint==62.1` version, but it pulls the **absolute latest** version of `pydyf` (which recently updated to `v0.11.0+`).
5. `pydyf` version `0.11.0` introduced breaking API changes that removed the `.transform()` method. `weasyprint==62.1` still expects this method to exist, causing an immediate runtime crash.

## Recommended Fix
We have two clean options to resolve this dependency conflict without modifying any application code.

**Option A (Recommended - Upgrade WeasyPrint):**
Upgrade `weasyprint` to a version that supports the new `pydyf` API.
Change `weasyprint==62.1` to `weasyprint>=63.0` in `requirements.txt`.

**Option B (Downgrade & Pin pydyf):**
Lock `pydyf` to the older API structure that `weasyprint==62.1` expects.
Add `pydyf<0.11.0` explicitly to `requirements.txt`.

Both options require only a single-line text change in `backend/requirements.txt` and a subsequent `docker-compose build` to permanently resolve the PDF generation failure.
