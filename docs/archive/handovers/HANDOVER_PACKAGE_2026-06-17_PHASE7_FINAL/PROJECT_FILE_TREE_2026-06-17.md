---
archive_title: "PROJECT FILE TREE"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PROJECT FILE TREE
**Generated:** 2026-06-18 16:32:42

## Summary
- **Total Files:** 219
- **Python Files:** 78
- **Test Files:** 28
- **Test Results:** 613 Passed, 0 Failed

## Repository Structure
`	ext
vedic-ai-system
├── docs/status/FINAL_REPOSITORY_TREE_AUDIT.md
├── docs/status/FINAL_TREE_PLACEMENT_AUDIT.md
├── app_tree.txt
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── api
│   │   │   └── v1
│   │   │       ├── endpoints
│   │   │       │   ├── charts.py
│   │   │       │   ├── health.py
│   │   │       │   ├── queries.py
│   │   │       │   └── reports.py
│   │   │       └── router.py
│   │   ├── archive_legacy_pdf_pipeline
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   └── astrology_constants.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   ├── database
│   │   ├── engines
│   │   │   ├── __init__.py
│   │   │   ├── ashtakavarga_engine.py
│   │   │   ├── dasha_engine.py
│   │   │   ├── functional_nature_engine.py
│   │   │   ├── house_strength_engine.py
│   │   │   ├── mandali_generator.py
│   │   │   ├── master_probability_engine.py
│   │   │   ├── natal_promise_engine.py
│   │   │   ├── planet_strength_engine.py
│   │   │   ├── quality_metrics_engine.py
│   │   │   ├── question_engine.py
│   │   │   ├── rasi_strength_engine.py
│   │   │   ├── transit_engine.py
│   │   │   ├── varga_engine.py
│   │   │   └── yoga_engine.py
│   │   ├── interpretations
│   │   ├── models
│   │   ├── parsers
│   │   │   ├── __init__.py
│   │   │   ├── horoscope_source_loader.py
│   │   │   └── json_normalizer.py
│   │   ├── pipeline_runner.py
│   │   ├── reports
│   │   │   ├── builder.py
│   │   │   ├── html_generator.py
│   │   │   ├── pdf_generator.py
│   │   │   ├── schemas.py
│   │   │   ├── sections
│   │   │   │   ├── base.py
│   │   │   │   └── extractors.py
│   │   │   └── templates
│   │   │       └── base.html
│   │   ├── schemas
│   │   │   ├── chart.py
│   │   │   └── question.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── astrology_math.py
│   │       └── ephemeris_service.py
│   ├── archive_legacy_pdf_pipeline
│   │   ├── debug_pdf_extract.py
│   │   ├── index_reader.py
│   │   ├── pdf_text_extractor.py
│   │   ├── table_parser.py
│   │   └── tests
│   │       ├── test_index_reader.py
│   │       ├── test_pdf_text_extractor.py
│   │       └── test_table_parser.py
│   ├── av_tables.txt
│   ├── av_tables2.txt
│   ├── debug
│   ├── inspect_av.py
│   ├── main.py
│   ├── requirements.txt
│   ├── run.py
│   ├── search_astakavarga.py
│   ├── test_output.txt
│   ├── test_output_script.py
│   ├── test_output_script2.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_accuracy_validation.py
│   │   ├── test_ashtakavarga_engine.py
│   │   ├── test_dasha_engine.py
│   │   ├── test_ephemeris_service.py
│   │   ├── test_functional_nature_engine.py
│   │   ├── test_horoscope_source_loader.py
│   │   ├── test_house_strength_sav.py
│   │   ├── test_json_normalizer.py
│   │   ├── test_mandali_generator.py
│   │   ├── test_master_probability_engine.py
│   │   ├── test_natal_promise_engine.py
│   │   ├── test_p1_fixes.py
│   │   ├── test_pipeline_runner.py
│   │   ├── test_planet_strength_engine.py
│   │   ├── test_quality_metrics.py
│   │   ├── test_question_engine.py
│   │   ├── test_rasi_strength_engine.py
│   │   ├── test_real_charts.py
│   │   ├── test_report_builder.py
│   │   ├── test_transit_engine.py
│   │   ├── test_varga_engine.py
│   │   ├── test_weightage_calibration.py
│   │   └── test_yoga_engine.py
│   ├── trace_chart.py
│   └── validation_check.txt
├── backend_tree.txt
├── docs
│   ├── ARCHITECTURE_RULES.md
│   ├── GOCHARA_MANDALI_GOVERNANCE_v1.md
│   ├── README_FIRST.md
│   ├── VEDIC_AI_SOURCE_OF_TRUTH.md
│   ├── archive
│   │   ├── ARCHITECTURE_CONTRADICTIONS_AND_CLARIFICATIONS.md
│   │   ├── AUTHORITY_LOCK_CONFIRMATION.md
│   │   ├── CHATGPT_ARCHITECTURE_MEMORY.md
│   │   ├── CHATGPT_IMPLEMENTATION_MEMORY.md
│   │   ├── ENGINE_BOUNDARY_VALIDATION.md
│   │   ├── GOCHARA_ARCHITECTURE_AUDIT.md
│   │   ├── JSON_CONTRACT_MASTER.md
│   │   ├── PROJECT_CONTEXT.md
│   │   ├── PROJECT_REQUIREMENTS.md
│   │   ├── PROJECT_STATUS_MASTER.md
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── VEDIC_AI_SYSTEM_MASTER_STATUS.md
│   │   ├── VEDIC_AI_VERIFIED_SOURCE_AUDIT.md
│   │   ├── audit
│   │   │   ├── BUG_VALIDATION_AUDIT.md
│   │   │   ├── DOCUMENTATION_INVENTORY_AUDIT.md
│   │   │   ├── ENGINE_OUTPUT_AUDIT.md
│   │   │   ├── FILE_MODIFICATION_VERIFICATION.md
│   │   │   ├── PHASE4_FIX_PLAN.md
│   │   │   ├── POST_FIX_VALIDATION.md
│   │   │   ├── PRIMARY_AUTHORITY_CONFLICT_AUDIT.md
│   │   │   ├── PYTHON_FILE_AUDIT.md
│   │   │   ├── README_FINAL_VALIDATION.md
│   │   │   ├── README_FIRST_VALIDATION.md
│   │   │   ├── REFERENCE_FOLDER_AUTHORITY_AUDIT.md
│   │   │   ├── RUNTIME_TRACE_AUDIT.md
│   │   │   ├── SAFE_CLEANUP_REPORT.md
│   │   │   ├── project_tree_after_cleanup.txt
│   │   │   └── walkthrough.md
│   │   └── gocharm_lagacy
│   │       ├── GOCHARA_ENGINE_MASTER.md
│   │       ├── GOCHARA_OUTPUT_TEMPLATES.md
│   │       └── GOCHARA_TEST_CASES.md
│   ├── current_status
│   │   ├── IMPLEMENTATION_PROGRESS_TRACKER_2026-06-12_IST.md
│   │   ├── PHASE7_COMPLETION_REPORT_2026-06-17_1305.md
│   │   ├── PROJECT_FILE_TREE_2026-06-17.md
│   │   ├── PROJECT_HANDOVER_2026-06-17_1305.md
│   │   ├── PROJECT_HANDOVER_MASTER_2026-06-09_13-45_IST.md
│   │   ├── RELEASE_READINESS_AUDIT_2026-06-17_1305.md
│   │   └── VEDIC-AI SYSTEM – PROJECT HANDOVER STATUS (June 2026).md
│   ├── docs
│   │   └── samartha_v2
│   │       ├── CANONICAL_JSON_SCHEMA.md
│   │       ├── CAUTIONS.md
│   │       ├── FORMULA_REGISTRY.md
│   │       ├── MODULE_BOUNDARIES.md
│   │       ├── QUESTIONNAIRE_PIPELINE.md
│   │       ├── RUNTIME_FALLBACKS.md
│   │       ├── SYSTEM_RULES_CORE.md
│   │       ├── caliculatio_engine_arch.md
│   │       ├── index.html
│   │       └── raju_canonical_content.json
│   ├── governance
│   │   ├── AUTHORITY_LOCK_2026-06-11_18-15_IST.md
│   │   ├── CODING_AGENT_MEMORY_2026-06-11_IST.md
│   │   ├── CODING_AGENT_PRECAUTIONS.md
│   │   ├── CONTRACT_REGISTRY.md
│   │   ├── DECISION_REGISTER.md
│   │   ├── FUNCTIONAL_NATURE_GOVERNANCE_LOCK.md
│   │   ├── PROJECT_DOCUMENT_INDEX.md
│   │   ├── PROJECT_GOVERNANCE_SUMMARY.md
│   │   ├── PROJECT_REFERENCE_MASTER_2026-06-11_IST.md
│   │   └── READ_THIS_FIRST_NEW_CHAT.md
│   ├── implementation
│   │   ├── ENGINE_INPUT_OUTPUT_MAP.md
│   │   ├── EXTRACTION_EXPANSION_PLAN.md
│   │   ├── EXTRACTION_FEASIBILITY_REPORT.md
│   │   ├── FUNCTIONAL_NATURE_ENGINE_DESIGN.md
│   │   ├── FUNCTIONAL_NATURE_ENGINE_FINAL_DESIGN.md
│   │   ├── NEXT_IMPLEMENTATION_PLAN.md
│   │   ├── QUESTION_ENGINE_FINAL_REFACTOR_DESIGN.md
│   │   └── SAMARTHA_GOCHARA_IMPLEMENTATION_BLUEPRINT.md
│   ├── reference
│   │   ├── CANONICAL_DATA_INVENTORY.md
│   │   ├── IMPLEMENTATION_GAP_REPORT.md
│   │   ├── PROJECT_CONTEXT.md
│   │   ├── PROJECT_REQUIREMENTS.md
│   │   ├── VEDIC_AI_MASTER_ARCHITECTURE.md
│   │   ├── VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md
│   │   ├── VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md
│   │   └── VEDIC_AI_docs/status/VERSION_1_RELEASE.md
│   └── validation
│       ├── ASTROLOGY_VALIDATION_MASTER_PLAN.md
│       ├── IMPLEMENTATION_DEPENDENCY_MAP.md
│       ├── NATAL_PROMISE_VALIDATION_AUDIT.md
│       ├── PROJECT_MILESTONE_v1_RUNTIME_VALIDATION.md
│       └── VEDIC_RULE_VALIDATION_REVIEW.md
├── docs_tree.txt
├── extracted_json
│   ├── canonical_content.json
│   └── machine_index.json
├── frontend
│   ├── README.md
│   ├── dist
│   │   ├── assets
│   │   │   ├── index-8vvDIOpj.js
│   │   │   └── index-BZaXZ_5W.css
│   │   ├── favicon.svg
│   │   ├── icons.svg
│   │   ├── index.html
│   │   ├── manifest.webmanifest
│   │   ├── registerSW.js
│   │   ├── sw.js
│   │   └── workbox-9c191d2f.js
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── public
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── src
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── api
│   │   │   └── backend.ts
│   │   ├── assets
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   ├── components
│   │   │   └── layout
│   │   │       └── Layout.tsx
│   │   ├── index.css
│   │   ├── main.tsx
│   │   ├── pages
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ExportReport.tsx
│   │   │   ├── QuestionEngine.tsx
│   │   │   ├── Results.tsx
│   │   │   └── Upload.tsx
│   │   ├── store
│   │   │   └── useChartStore.ts
│   │   └── types
│   │       └── schema.d.ts
│   ├── tailwind.config.js
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── git_status_snapshot.txt
├── outputs
├── project_tree.txt
├── pytest.ini
├── sample_reports
│   └── raju_cleaned.pdf
├── source_pdfs
│   ├── full_horoscope.pdf
│   └── source_index.pdf
└── temp
    └── project_tree.txt
`
