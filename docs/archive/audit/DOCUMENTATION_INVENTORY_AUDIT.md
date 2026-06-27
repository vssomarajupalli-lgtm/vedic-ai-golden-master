# DOCUMENTATION INVENTORY AUDIT

## File Inventory

| File Path | Purpose | Current Status |
| :--- | :--- | :--- |
| `BUG_VALIDATION_AUDIT.md` | Summary of reproducible evidence and technical validations for logic bugs. | REFERENCE |
| `ENGINE_OUTPUT_AUDIT.md` | Mathematical audit of the seven computational engines processing the canonical chart. | REFERENCE |
| `FILE_MODIFICATION_VERIFICATION.md` | Verification audit of active vs obsolete status of Python files for the Safe Cleanup Phase. | REFERENCE |
| `PHASE4_FIX_PLAN.md` | Outline of the step-by-step implementation plan to resolve computational bugs in the engines. | REFERENCE |
| `POST_FIX_VALIDATION.md` | Validation summary comparing engine outputs before and after applying computational fixes. | REFERENCE |
| `PYTHON_FILE_AUDIT.md` | Codebase audit summary of Python files, mapping usage, classifications, and duplication risks. | REFERENCE |
| `RUNTIME_TRACE_AUDIT.md` | Audit tracing the data structure and key counts at each step of the execution flow. | REFERENCE |
| `SAFE_CLEANUP_REPORT.md` | Report detailing the execution and verification of the Safe Cleanup Phase archiving legacy files. | REFERENCE |
| `walkthrough.md` | Walkthrough summarizing Phase 4 fix execution, testing verification, and validation results. | REFERENCE |
| `docs/ARCHITECTURE_RULES.md` | Defines the active architectural rules for the current implementation phase. | ACTIVE |
| `docs/ASTROLOGY_VALIDATION_MASTER_PLAN.md` | Validates mathematical calculations and scoring heuristics against classical texts. | REFERENCE |
| `docs/CHATGPT_IMPLEMENTATION_MEMORY.md` | Obsolete memory document from Runtime Investigation Phase (June 2026). | OBSOLETE |
| `docs/IMPLEMENTATION_DEPENDENCY_MAP.md` | Maps implementation dependencies for missing and oversimplified astrological rules. | REFERENCE |
| `docs/NATAL_PROMISE_VALIDATION_AUDIT.md` | Technical and astrological audit of the NatalPromiseEngine across all eight life domains. | REFERENCE |
| `docs/PROJECT_MILESTONE_v1_RUNTIME_VALIDATION.md` | Documents the completion of the Runtime Validation Milestone. | REFERENCE |
| `docs/README_FIRST.md` | Important instructions and document reading order for new developers. | ACTIVE |
| `docs/SYSTEM_ARCHITECTURE.md` | Obsolete architecture document identical to CHATGPT_IMPLEMENTATION_MEMORY.md. | OBSOLETE |
| `docs/VEDIC_AI_SOURCE_OF_TRUTH.md` | Defines the official source assets consumed by Vedic-AI. | ACTIVE |
| `docs/VEDIC_RULE_VALIDATION_REVIEW.md` | Reviews proposed astrological enhancements for the computational engines. | REFERENCE |
| `docs/VEDIC-AI SYSTEM – PROJECT HANDOVER STATUS (June 2026).md` | Project Handover Status showing current backend/frontend status and action plan. | ACTIVE |
| `docs/archive/CHATGPT_ARCHITECTURE_MEMORY.md` | Historical architecture memory document. | ARCHIVED |
| `docs/archive/CHATGPT_IMPLEMENTATION_MEMORY.md` | Historical implementation memory document emphasizing PDF extraction. | ARCHIVED |
| `docs/archive/JSON_CONTRACT_MASTER.md` | Historical definition of the JSON contract philosophy and normalized payload structure. | ARCHIVED |
| `docs/archive/PROJECT_CONTEXT.md` | Historical project context focusing on PDF extraction. | ARCHIVED |
| `docs/archive/PROJECT_REQUIREMENTS.md` | Historical project requirements emphasizing PDF extraction. | ARCHIVED |
| `docs/archive/PROJECT_STATUS_MASTER.md` | Historical status document from the Runtime Investigation Phase. | ARCHIVED |
| `docs/archive/SYSTEM_ARCHITECTURE.md` | Historical system architecture focusing on PDF extraction workflow. | ARCHIVED |
| `docs/archive/VEDIC_AI_SYSTEM_MASTER_STATUS.md` | Historical master status showing early completion estimates. | ARCHIVED |
| `docs/archive/VEDIC_AI_VERIFIED_SOURCE_AUDIT.md` | Historical audit of the verified source tree and implementations. | ARCHIVED |
| `docs/reference/PROJECT_CONTEXT.md` | Describes what Vedic-AI is, current phase, tech stack, and core directives. | ACTIVE |
| `docs/reference/PROJECT_REQUIREMENTS.md` | Defines Version 1 and Version 2 capabilities and non-functional requirements. | ACTIVE |
| `docs/reference/VEDIC_AI_MASTER_ARCHITECTURE.md` | The Master Architecture Document outlining core engines, technical layers, and vision. | ACTIVE |
| `docs/reference/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` | Detailed development roadmap for data ingestion, engines, and domain evaluation. | ACTIVE |
| `docs/reference/VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` | Master calculation document defining formulas and weighting for the probability engines. | ACTIVE |
| `docs/reference/VEDIC_AI_VERSION_1_RELEASE.md` | Release notes for Version 1.0.0 (Phase 4 Freeze). | ACTIVE |
| `frontend/README.md` | Default Vite/React README with ESLint setup instructions. | ACTIVE |

## Specific Queries

**A. Which file should be read first by a new developer.**  
`docs/README_FIRST.md`

**B. Which file is the master architecture document.**  
`docs/reference/VEDIC_AI_MASTER_ARCHITECTURE.md`

**C. Which file is the master calculation document.**  
`docs/reference/VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md`

**D. Which file is the master project status document.**  
`docs/VEDIC-AI SYSTEM – PROJECT HANDOVER STATUS (June 2026).md`

**E. Which files should never be used for implementation because they are historical only.**  
All files within the `docs/archive/` directory, as well as the obsolete root-level files `docs/CHATGPT_IMPLEMENTATION_MEMORY.md` and `docs/SYSTEM_ARCHITECTURE.md` (which are unpatched legacy state duplicates).

**F. Any README links that point to obsolete documents.**  
Yes, `docs/README_FIRST.md` lists `CHATGPT_IMPLEMENTATION_MEMORY.md` as #3 in the reading order and claims that `PROJECT_STATUS_MASTER.md` overrides older documents. Both of these documents are now obsolete/archived and do not reflect the current system state.
