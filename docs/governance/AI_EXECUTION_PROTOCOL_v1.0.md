# AI Execution Protocol v1.0

Generated: 2026-07-18 10:45:00
Updated: 2026-07-18 10:50:00

---

## Permanent Rules

### 1. Governance Authority

- Always follow the latest approved governance document for the current project phase.
- If multiple governance documents exist, the newest approved document takes precedence.

### 2. File Creation

- Do not create files unless the prompt explicitly requests them.
- If a new repository file is required but not explicitly requested, stop and ask for approval.

### 3. AI-Generated Supporting Artifacts

Only files **NOT intended to become part of the official Version 1.0 repository** shall be treated as AI-generated supporting artifacts.

Examples:
- Temporary analysis
- Scratch notes
- Intermediate audit outputs
- Comparison reports
- One-time investigation logs
- Experimental summaries
- Helper files created only to complete the current task

These files:

- Must end with `_ARTIFACT` in the filename.
- Must **NOT** be added using `git add` unless the Chief Architect explicitly approves them.
- Must **NOT** be treated as official project documentation.
- Must contain:
  - Prompt Number
  - Date
  - Time
  - Reason for creation
- Must be listed in the Repository Change Summary.

### 4. Official Project Deliverables

Files explicitly requested as part of the Version 1.0 repository are official deliverables.

Examples:
- Source code
- Configuration files
- Governance documents
- Release reports
- Validation workbooks
- Calibration logs
- Bug registers
- User documentation

These files:

- Use their official filenames.
- Must NOT use `_ARTIFACT`.
- May be committed to Git after approval.

### 5. Git Safety

- Never modify `.gitignore` automatically.
- Only recommend changes.
- Never stage or commit files without approval.

### 6. Repository Change Summary

At the end of every session report:

- Files Created
- Files Modified
- Files Deleted
- Files Renamed
- Artifact Files Created
- Files Recommended for Git
- Files Not Recommended for Git

### 7. Scope Control

Remain within the approved project scope.
If a request would expand scope, stop and request approval before proceeding.

---

## Additional Permanent Rules (GM-007 GOV-002)

### 8. Instruction Priority

When instructions conflict, follow them in this order:

1. Chief Architect's current prompt
2. Latest approved Governance document
3. AI_EXECUTION_PROTOCOL_v1.0.md
4. Other approved repository documents
5. Historical documents
6. AI default behaviour

If conflicts remain unresolved, stop and request clarification.

### 9. Repository Protection

Do not:

- Move files
- Rename files
- Delete files
- Archive files
- Reorganize folders

unless explicitly instructed.

### 10. Feature Freeze Compliance

While Version 1.0 remains under Feature Freeze, only the following work is permitted:

- Validation
- Calibration
- Confirmed Bug Fixes
- Documentation
- Workflow Improvements
- Report Improvements
- Stability Improvements

Do not introduce new functionality without explicit approval.

### 11. Repository Source of Truth

The Git repository is the only Source of Truth.

Do not rely on:

- Previous conversations
- AI memory
- Assumptions
- Temporary files

when repository documents are available.

### 12. Change Classification

Every recommendation must be classified as one of:

- Bug Fix
- Calibration
- Documentation
- Workflow
- Usability
- Validation
- Out of Scope

### 13. Architecture Decision Protection

Previously approved architecture decisions shall remain valid until superseded by a newer approved governance document.

Do not reopen previously approved decisions unless explicitly requested.

### 14. Single Source of Truth Principle

Whenever a deterministic formula, parameter, weight, planet strength, bhava strength, or calibration value changes, all dependent calculations, reports, PDFs, API responses, and UI displays must automatically use the updated value from the approved Single Source of Truth.

Duplicate implementations of deterministic calculations are prohibited.

### 15. AI Supporting Artifact Rule (Clarification)

_ARTIFACT files are temporary working files only.

They:

- Are NOT repository deliverables
- Are NOT official documentation
- Shall NOT be staged using `git add`
- Shall NOT be committed

unless explicitly approved by the Chief Architect.

---

## Deliverable

This document resides at:

`docs/governance/AI_EXECUTION_PROTOCOL_v1.0.md`

Do not create placeholder, audit, temporary, or helper files unless explicitly requested.