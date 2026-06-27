# ARCHITECTURE DECISION RECORD

**SNAPSHOT DATE:** 2026-06-20
**SNAPSHOT TIME:** 22:30 IST

## 1. Question Engine
*   **Decision:** The Question Engine is strictly defined as `Natal Promise + Dasha Activation`.
*   **Reason:** Enforces Parashari principle that Dasha delivers natal promise; prevents ephemeris calculation bottlenecks.
*   **Alternatives Rejected:** Including Transit (Mandali) within the Question Engine Boolean matrix.
*   **Impact:** Massive performance gain; perfect separation of concerns.

## 2. Formula Inheritance
*   **Decision:** Formulas inherit via `parent_formula_key` utilizing a dynamic merge (Parent overwrites Child).
*   **Reason:** Prevents massive JSON duplication. Base families hold standard signals; variants inject specific flags.
*   **Impact:** Highly scalable, DRY code for astrological rules.

## 3. Many-To-One Mapping
*   **Decision:** 500+ Questions map to 44 Formula Keys.
*   **Reason:** Questions like "Will I get a promotion?" and "When is my next increment?" share the identical astrological logic (`CAR_PROMOTION_TIMING`).
*   **Impact:** Decoupled UX presentation from backend astrology logic.

## 4. Formula Families
*   **Decision:** Domains are organized into Base Families (e.g. `AST_PROPERTY_BASE`) and Variants (`AST_PROP_TIMING`, `AST_PROP_LOSS_RISK`).

## 5. Governance Layers
*   **Decision:** Layer 1 (Promise), Layer 2 (Dasha), Layer 3 (Question), Layer 4 (Mandali). No crossover scoring allowed.

## 6. Mandali Separation
*   **Decision:** Mandali decoupled into an independent JSON advisory overlay.
*   **Reason:** Protects mathematical probability logic from real-time transit noise.
*   **Alternatives Rejected:** "Double-Transit Theory" embedded inside probability gates.

## 7. Evaluate Once Consume Many
*   **Decision:** LLM uses `AnswerComposer` to ingest deterministic JSON, never doing math itself.
*   **Reason:** Prevents LLM hallucinations on astrological calculations.

## 8. Loader Resolution
*   **Decision:** Loaders dynamically fetch Base and merge Variant.
*   **Impact:** Simplifies Python architecture.

## 9. Registry Design
*   **Decision:** `registry_data.py` defines schemas, `question_registry.json` defines routing.
