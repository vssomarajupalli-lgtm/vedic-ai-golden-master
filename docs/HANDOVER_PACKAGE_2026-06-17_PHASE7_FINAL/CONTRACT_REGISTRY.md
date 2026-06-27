# CONTRACT REGISTRY
**Date:** 2026-06-17 13:05 IST

### 1. JsonNormalizer Contract
- **Source:** JSON Payload
- **Consumers:** All Pipeline Engines
- **Required Fields:** `planets`, `houses`, `birth_data`
- **Prohibited Changes:** Altering standard keys or removing dignity mappings.

### 2. Dasha Timeline Contract
- **Source:** Dasha Engine
- **Consumers:** Master Probability Engine, Question Engine
- **Required Fields:** `timeline[]` list of chronological objects.
- **Prohibited Changes:** Reverting to a legacy flat mapping structure.

### 3. Transit Payload Contract
- **Source:** Transit Engine
- **Consumers:** Master Probability Engine
- **Required Fields:** `activation_score`
- **Prohibited Changes:** Changing the default stub generation logic.

### 4. Mandali Generator Contract
- **Source:** Mandali Generator
- **Consumers:** Transit Engine
- **Required Fields:** Absolute Pada indexing (1-108).
- **Prohibited Changes:** Altering the 12 Mandali mapping rules.

### 5. Functional Nature Contract
- **Source:** Functional Nature Engine
- **Consumers:** Pipeline Runner
- **Required Fields:** Classification as `benefic`, `malefic`, or `neutral`.
- **Prohibited Changes:** Allowing dynamic logic overriding structural rules.

### 6. Dosha Routing Contract
- **Source:** Dosha Passthrough
- **Consumers:** Question Engine
- **Required Fields:** Dosha status keys natively mapped.
- **Prohibited Changes:** Creating new dosha score penalties.

### 7. Question Engine Contract
- **Source:** Question Engine
- **Consumers:** Report Builder, Frontend
- **Required Fields:** Accurate referencing of Natal Promise domain scoring.
- **Prohibited Changes:** Hallucinating domains without engine validation.

### 8. Report Builder Contract
- **Source:** Pipeline Outputs
- **Consumers:** PDF Generation, Frontend Results
- **Required Fields:** `master_probability` section containing final_score.
- **Prohibited Changes:** Altering presentation hierarchies.
