# ADR INVENTORY v1.0
**Context:** Golden Master Refinement (GM-005) - BKL-005 Scope Freeze
**Status:** Under Review

This document inventories hidden architectural constraints and rules extracted from legacy Phase 8 through Phase 16 reports. These candidates represent critical system constraints that must be preserved as formal Architecture Decision Records (ADRs) to prevent knowledge loss during repository archival.

---

### Candidate ID: ADR-CAND-001
* **Proposed ADR Title:** Formula Scaling via Many-to-One Convergence Rule
* **Source Document(s):** `PHASE14C_CATALOG_ARCHITECTURE_REPORT.md`, `PHASE14E_IMPLEMENTATION_REPORT.md`, `docs/governance/PHASE14D_RISK_REGISTER.md`
* **Repository Evidence:** "- Confirmed via the mapping constraint ensuring ~500 Question IDs converge down to ~100 Formula Variants, which in turn inherit from ~35 Base Formula Families."
* **Short Description:** Mandates that new UI Question IDs map to existing formula variants instead of creating 1-to-1 duplicated math logic.
* **Why this requires an ADR:** This prevents formula explosion and repository bloat. Without it, developers may incorrectly create duplicate math definitions for semantically similar questions.
* **Architectural Category:** Formula Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-002
* **Proposed ADR Title:** Prohibition of LLM-Driven Astrological Decision Making
* **Source Document(s):** `PHASE14C_CATALOG_ARCHITECTURE_REPORT.md`
* **Repository Evidence:** "- **No LLM decision making:** Confirmed."
* **Short Description:** The LLM acts purely as a formatter and is strictly forbidden from executing or inferring astrological math.
* **Why this requires an ADR:** Protects the deterministic integrity of the Golden Master. If an LLM executes logic, the system loses determinism.
* **Architectural Category:** Engine Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-003
* **Proposed ADR Title:** Exclusion of the Moon from the Biological Progeny Promise
* **Source Document(s):** `PHASE14G_HARDENING_REVIEW.md`
* **Repository Evidence:** "The Moon rules the mind and emotions. While it plays a role in female fertility, the primary Parashari indicators for the creation of offspring are the 5th house and Jupiter. Adding the Moon dilutes the physical promise of a child with emotional desire..."
* **Short Description:** Mandates that the Moon not be used as a primary structural factor in calculating the physical promise of children.
* **Why this requires an ADR:** Documents a highly specific, hard-won domain modeling choice that future astrologers might accidentally revert.
* **Architectural Category:** Data Model / Formula Logic
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-004
* **Proposed ADR Title:** Prohibition of Aggregating Promise, Dasha, and Transit Scores
* **Source Document(s):** `PHASE15A_ENGINE_INTERFACE_AUDIT.md`
* **Repository Evidence:** "*Warning:* This component inherently violates the Phase 15 frozen governance rule (forbidden combination of Promise + Dasha + Transit into a single score)."
* **Short Description:** Forbids flattening Natal Promise (static), Dasha (timing), and Transit (current sky) values into one unified mathematical score.
* **Why this requires an ADR:** This is a fundamental structural limit of the Vedic-AI architecture ensuring layered temporal analysis is preserved over simple math.
* **Architectural Category:** Engine Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-005
* **Proposed ADR Title:** Formula Final State Supremacy (Strict Tone-Locking)
* **Source Document(s):** `PHASE15A_ENGINE_INTERFACE_AUDIT.md`, `PHASE13D_COMPOSER_ARCHITECTURE_REPORT.md`
* **Repository Evidence:** "Strict System Prompting must be enforced in the templates to mandate that the Formula's `FINAL STATE` is absolute law."
* **Short Description:** The pre-calculated mathematical output (the Final State) dictates the absolute tone and answer for the LLM.
* **Why this requires an ADR:** Prevents LLM hallucinations where prompt phrasing might override actual calculations.
* **Architectural Category:** Validation / Pipeline
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-006
* **Proposed ADR Title:** Mandali as an Interpretive Overlay (Decoupled from Core Math)
* **Source Document(s):** `PHASE15_PREPARATION_REPORT.md`
* **Repository Evidence:** "Phase 15 transitions Mandali from a *Mathematical Constraint* (which crashes formulas if missing) into an *Interpretive Overlay* (which enriches the final natural language answer)."
* **Short Description:** Restricts Mandali from mutating the core True/False logic of a formula; it provides nuance, not core validation.
* **Why this requires an ADR:** Explains a major architectural pivot (Phase 15 decouple) ensuring Mandali failures don't crash core timing analysis.
* **Architectural Category:** Engine Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-007
* **Proposed ADR Title:** The 24 Master Node to 200+ Question Expansion Blueprint
* **Source Document(s):** `PHASE9_QUESTION_BLUEPRINT_UPDATE_REPORT.md`
* **Repository Evidence:** "...locking the "24 Master Nodes → 200+ Child Questions" architectural rule and the 12-Bhava routing approach."
* **Short Description:** Mandates the hierarchical approach to organizing UI questions through 24 fixed astrological domains.
* **Why this requires an ADR:** Defines the exact routing skeleton that governs how frontend questions map to backend logic.
* **Architectural Category:** Engine Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-008
* **Proposed ADR Title:** Prohibition of Hardcoded Astrological Rules
* **Source Document(s):** `docs/governance/PHASE9_STEP3A_GOVERNANCE_PACKAGE_REPORT_2026-06-19_1130.md`
* **Repository Evidence:** "`FORMULA_REPOSITORY_DESIGN` strictly forbids hardcoded astrology rules inside Python execution code, pushing rule evaluation to an externalized format."
* **Short Description:** Requires all new mathematical astrological structures to be defined externally (YAML/JSON) rather than compiled into Python classes.
* **Why this requires an ADR:** Prevents backend monoliths and preserves the "Engine = Math execution only" boundary.
* **Architectural Category:** Governance
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-009
* **Proposed ADR Title:** Evaluate Once, Consume Many (Single Source of Truth)
* **Source Document(s):** `PHASE12A_FORMULA_ARCHITECTURE_REPORT.md`, `PHASE14A_ARCHITECTURE_REPORT.md`
* **Repository Evidence:** "Detailed the 'Evaluate Once, Consume Many' dependency mapping for the computational engines... Downstream systems are strictly forbidden from recalculating astrology."
* **Short Description:** Forces the Formula Evaluator to be the solitary executor of math. All downstream systems (UI, PDF, LLM) must consume its exact boolean payload.
* **Why this requires an ADR:** Protects against fragmented logic where the UI calculates one output and the backend calculates another.
* **Architectural Category:** Engine Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-010
* **Proposed ADR Title:** Answer Composer Firewall Rules
* **Source Document(s):** `PHASE12A_FORMULA_ARCHITECTURE_REPORT.md`
* **Repository Evidence:** "- Defined the firewall rules for the Answer Composer to prevent LLM hallucinations (Context Injection bounding, Evaluation Overriding prohibition, Tone enforcement)."
* **Short Description:** Establishes specific input-bounding boundaries that the Answer Composer API must enforce.
* **Why this requires an ADR:** Defines the critical safety perimeter guarding LLM usage in production astrology.
* **Architectural Category:** Validation / Pipeline
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-011
* **Proposed ADR Title:** Graceful Degradation via MIXED State Capping
* **Source Document(s):** `PHASE13B_EVALUATOR_ARCHITECTURE_REPORT.md`
* **Repository Evidence:** "- Established the protocol for capping results at `MIXED` if a required engine (like `TransitEngine`) fails, mitigating systemic outages."
* **Short Description:** If an external engine drops out, the system degrades to a MIXED state rather than generating a false positive or fully crashing.
* **Why this requires an ADR:** Documents a critical resilience mechanism for production stability.
* **Architectural Category:** Evaluation / Pipeline
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-012
* **Proposed ADR Title:** Deterministic Communication of System Warnings
* **Source Document(s):** `PHASE13D_COMPOSER_ARCHITECTURE_REPORT.md`
* **Repository Evidence:** "- I recommended the **Deterministic** approach (Alternative B) because relying on the LLM to communicate system failures invites hallucination and violates our mandate for explicit determinism."
* **Short Description:** Mandates that missing data warnings (e.g. "Transit Data Unavailable") are appended deterministically rather than generated by the LLM.
* **Why this requires an ADR:** Fixes a UI edge case while preserving strict prompt-bounding logic.
* **Architectural Category:** Validation / UI
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-013
* **Proposed ADR Title:** YAML as the Canonical Formula Storage Format
* **Source Document(s):** `PHASE10A_FORMULA_LOADER_BLUEPRINT_2026-06-19.md`
* **Repository Evidence:** "**YAML** is the strictly recommended format for the Formula Repository... A Python registry (`formulas.py`) invites the temptation to write executable logic..."
* **Short Description:** Establishes YAML as the standard configuration file type over JSON or Python for formula definition due to readability and decoupling.
* **Why this requires an ADR:** Prevents fragmentation and establishes standard developer tooling requirements for formulas.
* **Architectural Category:** Repository Structure
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-014
* **Proposed ADR Title:** Single JSON Array Format for Question Registry
* **Source Document(s):** `PHASE11A_REGISTRY_IMPLEMENTATION_REPORT.md`
* **Repository Evidence:** "- **Format:** JSON Array / - **Schema Compliance:** Each entry strictly mirrors the approved Phase 9 mapping schema"
* **Short Description:** Mandates `question_registry.json` strictly as a schema-compliant JSON array to facilitate high-speed O(1) hash mapping during API routing.
* **Why this requires an ADR:** Freezes the foundational data format for the frontend-to-backend communication layer.
* **Architectural Category:** Repository Structure
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-015
* **Proposed ADR Title:** Deterministic Mapping Matrix (Replacement of NLP Routing)
* **Source Document(s):** `PHASE9_STEP3B_REGISTRY_DATA_MODEL_REPORT.md`
* **Repository Evidence:** "The hierarchical data dictionary strictly binds frontend user queries to backend mathematical engine logic, replacing fragile NLP intent matching with a deterministic mapping matrix."
* **Short Description:** The application explicitly uses hard-mapped IDs rather than Generative NLP to route a user's question to a mathematical formula.
* **Why this requires an ADR:** Documents a massive architectural shift prioritizing safety over generative query flexibility.
* **Architectural Category:** Engine Architecture
* **Current Status:** Candidate

---

### Candidate ID: ADR-CAND-016
* **Proposed ADR Title:** Non-Numeric Confidence Model (Boolean Layering)
* **Source Document(s):** `PHASE12B_DATA_MODEL_REPORT.md`
* **Repository Evidence:** "- Designed the conceptual Confidence Model, outlining how 5 distinct layers... contribute to the validity of an astrological prediction without utilizing raw numeric scoring yet."
* **Short Description:** Evaluation relies on logical AND/OR gating (Fatal Denials vs. Positive Alignment) rather than arbitrary numeric weights (e.g. +15% per planet).
* **Why this requires an ADR:** Locks in the core philosophical approach to the mathematical evaluation layer.
* **Architectural Category:** Data Model / Formula Logic
* **Current Status:** Candidate
