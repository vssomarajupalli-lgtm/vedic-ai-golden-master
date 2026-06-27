# IMPLEMENTATION GAP REPORT

This document cross-references the official Approved Master Roadmap against the actual physical files in `backend/app/engines` to identify implementations, stubs, missing logic, and dead code.

---

## 1. Engine Implementation Status

| Engine | Planned Phase | Implemented File | Missing / Gap | Status |
| :--- | :---: | :--- | :--- | :--- |
| **Data Layer** | Phase 1 | `json_normalizer.py` | None | **Complete** |
| **Ascendant Layer** | Phase 1 | `json_normalizer.py` (via metadata) | Missing isolated logic module for Functional Nature (Benefic/Malefic mapping). | **Partial** |
| **Planet Strength Engine** | Phase 1 | `planet_strength_engine.py` | None | **Complete** |
| **Rasi Strength Engine** | Phase 2 | `rasi_strength_engine.py` | None | **Complete** |
| **House Strength Engine** | Phase 2 | `house_strength_engine.py` | None | **Complete** |
| **Dosha Engine** | Phase 2 | None | Kuja Dosha, Kala Sarpa, and Pitru Dosha logic are completely missing. | **Missing** |
| **Yoga Engine** | Phase 2 | `yoga_engine.py` | None | **Complete** |
| **Shodasavarga Engine** | Phase 3 | `varga_engine.py` | Complete for D9 and D10. Missing advanced Vargas (D2, D4, D7, etc.). | **Partial** |
| **Natal Promise Engine** | Phase 3 | `natal_promise_engine.py` | Core domains exist, but specific classical variables (Beeja Sphuta, Upapada Lagna) from audit are absent. | **Complete** |
| **Dasha Extraction & Activation Engine** | Phase 4 | `dasha_engine.py` | Needs refactoring to ensure it behaves strictly as an extraction reader, per DR-001. | **Complete** |
| **Transit Engine (Gochara)** | Phase 5 | `transit_engine.py` | Currently implements fallback logic and structural stubs. Must be aligned with extraction-first mandate (DR-003). | **Stub** |
| **Domain Evaluation Engine** | Phase 5 | `natal_promise_engine.py` | Logical intent is merged into NatalPromise rather than isolated as its own Domain Evaluation Engine. | **Partial** |
| **Probability Engine** | Phase 5 | `master_probability_engine.py` | Event probability logic is consolidated inside the Master Synthesis. | **Partial** |
| **Question Engine** | Phase 5 | `question_engine.py` | Exists independently but is not formally linked directly inside the `PipelineRunner` synchronous flow. | **Partial** |
| **Master Synthesis Engine** | Phase 5 | `master_probability_engine.py` | None | **Complete** |
| **Remedy Engine** | Phase 6 | None | No logic exists for remedies. | **Missing** |

---

## 2. Risk Areas & Findings

### Existing Implementations
The core calculation matrix (Planet, House, Rasi, Yoga, Varga, NatalPromise, MasterProbability) is tightly coupled through the `PipelineRunner` and executes deterministically. The codebase demonstrates strong adherence to the "No Generative AI prediction" rule.

### Partial Implementations
The **Ascendant Layer** is functionally working as a metadata passthrough in the JSON Normalizer, but the roadmap indicates a robust `Functional Nature Engine` mapping (Benefic vs Malefic by Ascendant). This is a critical mathematical missing link.

### Missing Components
The **Dosha Engine** is entirely absent from the codebase. Important penalty computations like Kuja Dosha are currently skipped, leading to artificially elevated relationship/marriage probabilities.

### Duplicate Logic / Architectural Overlaps
The **Domain Evaluation Engine** and **Event Probability Engine** are explicitly listed as unique modules in the Phase 5 roadmap, but their physical responsibilities have been absorbed by `natal_promise_engine.py` and `master_probability_engine.py`. This isn't necessarily dead code, but an architectural blur that needs to be acknowledged.

### Dead Code / Stubs
**`transit_engine.py`** is functionally an empty stub (`_stub_result` returns 50 neutral) waiting for ephemeris payload connections. As per the new Gochara guidelines, this engine must be restructured to ingest canonical PDF transit findings before attempting raw ephemeris math.
