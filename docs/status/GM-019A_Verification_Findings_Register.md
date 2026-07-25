# GM-019A Verification Findings Register

## Verified Facts

1. **API Boundary**
   The backend correctly validates canonical inputs against the deterministic schema, successfully isolating the computational engines from PDF parsing logic.

2. **Presentation Path (Structural)**
   The frontend accurately receives and renders the backend's structural deterministic metrics, specifically Functional Nature, Natal Promise Scores, Ashtakavarga, and Rasi Strength.

3. **Knowledge Graph Generation**
   The backend generates Knowledge Graph entities. However, the `seed_default_data()` script instantiates some nodes without establishing structural relationships. The current integrity validation suite does not report these orphaned nodes.

4. **Computational Determinism**
   The `PipelineRunner` and the live `uvicorn` API lifecycle behave deterministically across isolated executions. Identical inputs reliably produce identical mathematical outputs.

5. **Temporal Input Contract**
   Verified that when `consultation_date` is omitted from the input payload, the pipeline resolves the target date from the system clock, and that this resolved date is subsequently consumed by the Dasha and Transit engines.

6. **Presentation Path (Temporal)**
   - **Gochara (Transit):** Follows a complete, unbroken end-to-end presentation path from backend generation to frontend rendering.
   - **Mandali:** Backend-generated Mandali data is produced, serialized, and received by the frontend. The current presentation component does not consume the backend Mandali payload and instead derives its displayed grid from Transit-related data.

---

## Identified Product Gaps

- **Graph Integrity:** The initial seeding process (`seed_default_data()`) creates disconnected entities, and the integrity validator does not flag orphaned nodes.
- **Mandali Presentation:** The frontend visualization bypasses the pre-calculated, mathematically validated Mandali structure generated and transmitted by the backend.
- **Temporal Input Consistency:** Because `consultation_date` is resolved internally when absent, the temporal inputs to deterministic engines are silently bound to the runtime clock rather than an explicit client-supplied date.
