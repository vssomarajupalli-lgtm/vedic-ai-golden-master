---
archive_title: "PHASE 7 ARCHITECTURAL LOCKS"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PHASE 7 ARCHITECTURAL LOCKS
**Document State:** Final (Phase 7 Lockdown)
**Date:** 2026-06-17

The following architectural principles and governance models are officially registered as **HARD LOCKS**. These rules protect the deterministic core of the Vedic AI System.

## 1. D1 Immutability Principle
* **Purpose:** Ensures the base natal chart (D1) remains the sole immutable source of truth for foundational planetary positions and relationships.
* **Protected Files:** `app/engines/planet_strength_engine.py`, `app/engines/house_strength_engine.py`
* **What must never change:** Vargas, Dashas, and Transits must NEVER mutate or overwrite D1 base scores. They act only as multipliers or capacity modifiers.
* **Why it exists:** To preserve structural integrity; if D1 is mutated, derived probabilistic calculations cascade into catastrophic mathematical errors.
* **Regression risks:** Allowing Varga engines to edit `canonical_content.json` directly.

## 2. Engine Isolation Principle
* **Purpose:** Enforces a Unidirectional Directed Acyclic Graph (DAG) flow.
* **Protected Files:** All files in `app/engines/`
* **What must never change:** Calculation engines must NEVER directly instantiate, call, or invoke each other.
* **Why it exists:** Prevents circular dependencies and hidden feedback loops that cause unpredictable scoring.
* **Regression risks:** An engine importing another engine directly rather than receiving data through the PipelineRunner.

## 3. PipelineRunner Orchestration Rule
* **Purpose:** Centralizes dependency injection and data flow management.
* **Protected Files:** `app/pipeline_runner.py`
* **What must never change:** The `PipelineRunner` is the absolute singular authority for orchestrating the execution sequence and passing payloads.
* **Why it exists:** Guarantees that engines fire in the exact sequential order required for valid outputs.
* **Regression risks:** Bypassing the PipelineRunner for "quick testing" or direct API route generation.

## 4. Varga Refinement Principle
* **Purpose:** Defines Vargas strictly as structural capacity modifiers.
* **Protected Files:** `app/engines/varga_engine.py`
* **What must never change:** Varga outputs must only scale or refine base probabilities. They cannot dictate independent events.
* **Why it exists:** Prevents fragmented, contradictory interpretations where D1 says "weak" and D9 says "strong" without a unified context.
* **Regression risks:** Treating Varga outputs as standalone charts for event prediction.

## 5. Dosha Preservation Routing
* **Purpose:** Ensures Dosha calculations (Mangal, Kuja, etc.) bypass normal strength scaling.
* **Protected Files:** `app/parsers/json_normalizer.py`, `app/engines/dosha_engine.py`
* **What must never change:** Dosha payloads must passthrough normalization intact and be evaluated independently of planetary dignity.
* **Why it exists:** Dosha is a binary structural state (present/absent), not a gradient strength state.
* **Regression risks:** Applying Shadbala multipliers to Dosha checks.

## 6. Functional Nature Governance
* **Purpose:** Locks the deterministic math for identifying benefic vs. malefic roles.
* **Protected Files:** `app/engines/functional_nature_engine.py`
* **What must never change:** The rule logic dictating functional vs. natural benefics based on ascendant.
* **Why it exists:** Functional nature is the primary pivot for whether a high-strength planet is protective or destructive.
* **Regression risks:** LLM/AI hallucinations attempting to redefine classic ascendant lord rules.

## 7. Dasha Timeline Contract
* **Purpose:** Standardizes time-based multiplier application.
* **Protected Files:** `app/engines/dasha_engine.py`
* **What must never change:** Dasha outputs must be formatted as a `timeline[]` array contract, never as flat dictionaries.
* **Why it exists:** Ensures frontend components can easily iterate and render chronological charts.
* **Regression risks:** Outputting nested dictionaries that break the `MasterProbabilityEngine` wrapper.

## 8. Mandali Boundary Governance
* **Purpose:** Replaces Rasi boundaries with mathematically precise Mandali (Nakshatra Pada) boundaries for transit effects.
* **Protected Files:** `app/engines/transit_engine.py`, `app/engines/mandali_generator.py`
* **What must never change:** Transits trigger when entering a Mandali, NOT a Rasi sign.
* **Why it exists:** Delivers micro-precision timing for Gochara snapshot triggers.
* **Regression risks:** Reverting to generic 30-degree Rasi sign bounds for Gochara.

## 9. Question Engine Synthesis Flow
* **Purpose:** Maps user queries to specific mathematical domains.
* **Protected Files:** `app/engines/question_engine.py`
* **What must never change:** The engine must map directly to derived domain scores rather than executing free-form text generation.
* **Why it exists:** Guarantees deterministic, reproducible answers to astrological questions based entirely on the calculation engines.
* **Regression risks:** Allowing an LLM to generate an answer before domain scores are mapped.

## 10. Contract Registry Compliance
* **Purpose:** Maintains absolute schema alignment.
* **Protected Files:** `docs/governance/CONTRACT_REGISTRY.md`, all Engine Schemas.
* **What must never change:** A new engine feature cannot be merged if it violates its registered payload contract.
* **Why it exists:** Ensures JSON flow from `canonical_content.json` through the `PipelineRunner` to the frontend never hits a parsing error.
* **Regression risks:** Adding custom keys dynamically without updating the Pydantic/contract models.

## 11. Master Probability Dashboard Role
* **Purpose:** Acts as the final synthesis layer.
* **Protected Files:** `app/engines/master_probability_engine.py`
* **What must never change:** It must exclusively synthesize outputs from other engines and never perform its own raw planetary strength calculations.
* **Why it exists:** It is the aggregator. Calculating raw data here violates the Engine Isolation Rule.
* **Regression risks:** Adding "quick planetary checks" inside the Master Probability code.

## 12. Deterministic Architecture Requirement
* **Purpose:** Zero unpredictability.
* **Protected Files:** System-wide.
* **What must never change:** 100% of the mathematical scoring must be purely deterministic logic without generative AI interpolation.
* **Why it exists:** Astrology software requires exact, reproducible outputs for trust.
* **Regression risks:** Integrating LLM API calls directly inside the engine mathematics.

## 13. Zero Magic Numbers Rule
* **Purpose:** Centralizes all mathematical weights and thresholds.
* **Protected Files:** `app/config/astrology_constants.py`
* **What must never change:** Hardcoded numbers (e.g., `50.0`, `0.75`) must NEVER exist inside engine logic files.
* **Why it exists:** Enables global tuning and prevents orphaned variables.
* **Regression risks:** Developers typing raw floats in new mathematical functions.
