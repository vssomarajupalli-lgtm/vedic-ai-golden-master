# ENGINE INPUT-OUTPUT MAP

This document explicitly defines the boundaries, dependencies, and handoffs between all modules in the Samartha Astro-AI system.

---

### 1. Data Layer (`JsonNormalizer`)
*   **Inputs**: Raw parsed JSON from HoroscopeCleaner_Final.
*   **Outputs**: `normalized_payload` (Strict typed schema: planets, houses, dashas, vargas).
*   **Dependencies**: None.
*   **Upstream Sources**: External extraction pipeline.
*   **Downstream Consumers**: All subsequent Calculation Engines.

### 2. Ascendant Layer
*   **Inputs**: `normalized_payload` metadata.
*   **Outputs**: Lagna sign index.
*   **Dependencies**: None.
*   **Upstream Sources**: Data Layer.
*   **Downstream Consumers**: Used locally by `PipelineRunner` for transit contextualization.

### 3. Planet Strength Engine
*   **Inputs**: Per-planet dictionary from `normalized_payload["planets"]`.
*   **Outputs**: Base `final_score` and dignity factors per planet.
*   **Dependencies**: None.
*   **Upstream Sources**: Data Layer.
*   **Downstream Consumers**: House Strength Engine, Yoga Engine, Varga Engine, Dasha Engine, Rasi Strength Engine, Ashtakavarga Engine, Natal Promise Engine.

### 4. House Strength Engine
*   **Inputs**: Per-house dictionary from `normalized_payload["houses"]`, `lord_strength_score`.
*   **Outputs**: House `final_score` and quality modifiers.
*   **Dependencies**: Planet Strength Engine (for the lord's pre-calculated strength).
*   **Upstream Sources**: Data Layer, Planet Strength Engine.
*   **Downstream Consumers**: Yoga Engine, Natal Promise Engine.

### 5. Yoga Engine
*   **Inputs**: `normalized_payload`, `planet_results`, `house_results`.
*   **Outputs**: Yoga `final_score` and identified classical combinations.
*   **Dependencies**: Planet Strength Engine, House Strength Engine.
*   **Upstream Sources**: Data Layer, Planet & House Engines.
*   **Downstream Consumers**: Natal Promise Engine, Master Synthesis Engine.

### 6. Shodasavarga Engine (`VargaEngine`)
*   **Inputs**: `normalized_payload["vargas"]`, `planet_results`.
*   **Outputs**: Nested chart-centric modifiers (`D9`, `D10`).
*   **Dependencies**: Planet Strength Engine.
*   **Upstream Sources**: Data Layer, Planet Strength Engine.
*   **Downstream Consumers**: Rasi Strength Engine, Natal Promise Engine, Master Synthesis Engine.

### 7. Dasha Extraction & Activation Engine
*   **Inputs**: `normalized_payload["dashas"]`, `planet_results`.
*   **Outputs**: Mahadasha/Antardasha timing multipliers and confidence flags.
*   **Dependencies**: Planet Strength Engine.
*   **Upstream Sources**: Data Layer, Planet Strength Engine.
*   **Downstream Consumers**: Transit Engine, Master Synthesis Engine, Question Engine.

### 8. Rasi Strength Engine
*   **Inputs**: `normalized_payload`, `planet_results`, `varga_results`.
*   **Outputs**: Sign-by-sign environment strength matrix.
*   **Dependencies**: Planet Strength Engine, Shodasavarga Engine.
*   **Upstream Sources**: Data Layer, Planet & Varga Engines.
*   **Downstream Consumers**: Natal Promise Engine, Master Synthesis Engine.

### 9. Ashtakavarga Engine
*   **Inputs**: `normalized_payload["ashtakavarga"]`, `planet_results`.
*   **Outputs**: BAV/SAV point modifiers and bindu confidence flags.
*   **Dependencies**: Planet Strength Engine.
*   **Upstream Sources**: Data Layer, Planet Strength Engine.
*   **Downstream Consumers**: Natal Promise Engine, Transit Engine, PipelineRunner (BAV modifier injection).

### 10. Natal Promise Engine (Domain Promise Layer)
*   **Inputs**: `planet_results`, `house_results`, `rasi_results`, `varga_results`, `av_results`, `yoga_results`.
*   **Outputs**: 8 Life Domain base promise scores (Marriage, Career, Wealth, etc.).
*   **Dependencies**: Planet, House, Rasi, Varga, Ashtakavarga, Yoga Engines.
*   **Upstream Sources**: All foundational calculations.
*   **Downstream Consumers**: Transit Engine, Master Synthesis Engine, Question Engine.

### 11. Transit Engine (Gochara Layer)
*   **Inputs**: Contextualized `transit_payload` (from Ephemeris), `natal_payload`, `dasha_results`, `av_results`, `natal_promise_results`.
*   **Outputs**: Transit `activation_score`, obstructing/supporting factors, Domain transit activation map.
*   **Dependencies**: Ephemeris Service, Dasha Engine, Ashtakavarga Engine, Natal Promise Engine.
*   **Upstream Sources**: PipelineRunner, Dasha, AV, Natal Promise.
*   **Downstream Consumers**: Master Synthesis Engine.

### 12. Question Engine
*   **Inputs**: User `question` string, full `pipeline_output` (from PipelineRunner).
*   **Outputs**: Structured deterministic answer block with timing and probability limits.
*   **Dependencies**: Entire Pipeline.
*   **Upstream Sources**: PipelineRunner output.
*   **Downstream Consumers**: API / Frontend.

### 13. Master Synthesis Engine (`MasterProbabilityEngine`)
*   **Inputs**: Aggregated dictionary of all `engine_outputs`.
*   **Outputs**: Final Master Probability `%`, Grade, and combined supporting factors.
*   **Dependencies**: All Calculation Engines.
*   **Upstream Sources**: PipelineRunner.
*   **Downstream Consumers**: API / Frontend.

### 14. Dosha Engine
*   **Inputs**: *Missing Implementation*
*   **Outputs**: *Missing Implementation*
*   **Dependencies**: *Missing Implementation*

### 15. Domain Evaluation & Event Probability Engines
*   **Status**: These logical roles are currently merged inside the `NatalPromiseEngine` (for domains) and `MasterProbabilityEngine` (for events/synthesis).
