# ENGINE OWNERSHIP AND DATA CONTRACT REGISTRY

## SECTION 1: Document Information

* **Date**: 2026-06-28
* **Time**: 22:45 IST
* **Repository**: D:\vedic-ai-golden-master
* **Program**: Program A
* **Milestone**: GM-004
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

Deterministic systems require clear, unambiguous ownership to maintain accuracy, prevent drift, and ensure the integrity of the architecture. This Engine Ownership and Data Contract Registry establishes the fundamental law of data ownership within the Golden Master repository. 

Every major data object within the system has exactly one canonical owner. There is absolutely no duplicated ownership and no overlapping authority. 

---

## SECTION 3: Engine Ownership Registry

| Engine | Classification | Primary Responsibility | Canonical Owner | Consumes | Produces | Owns | Must Never Own |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Planet Engine** | Core Astrology | Computes astronomical positions and fundamental planetary strengths. | Core Engine Team | Ephemeris Data, Time/Location | Planetary Positions, Raw Strengths | Planet Strength | House Strengths, Varga Results |
| **House Engine** | Core Astrology | Calculates house cusps and house-specific strengths. | Core Engine Team | Planetary Positions, Time/Location | House Cusps, House Strengths | House Strength | Planet Strengths |
| **Varga Engine** | Core Astrology | Computes divisional chart (Varga) positions and derived strengths. | Core Engine Team | Planetary Positions | Varga Positions, Varga Strengths | Varga Results | Dasha Activations |
| **Dasha Engine** | Core Astrology | Calculates planetary periods (Dashas) and their active spans. | Core Engine Team | Moon Position, Varga Results | Dasha Periods, Sub-periods | Dasha Activation | Yoga Detections |
| **Yoga Engine** | Applied Astrology | Detects planetary combinations (Yogas) and evaluates their conditions. | Logic Engine Team | Planet Strengths, House Strengths | Yoga Detections, Yoga Strengths | Yoga Detection | Dosha Detections |
| **Dosha Engine** | Applied Astrology | Detects planetary flaws (Doshas) and evaluates their severity/cancellation. | Logic Engine Team | Planet Strengths, House Strengths | Dosha Detections, Dosha Severity | Dosha Detection | Yoga Detections |
| **Functional Nature Engine** | Applied Astrology | Determines the functional benefic/malefic nature of planets for a given chart. | Logic Engine Team | House Strengths, Planet Strengths | Functional Benefic/Malefic Status | Functional Nature | Probability Results |
| **Master Probability Engine** | Synthesis | Synthesizes all astrological data into probabilistic outcomes. | AI/ML Team | Yogas, Doshas, Functional Nature | Synthesized Probabilities | Probability Result | Raw Astrological Calculations |
| **Calibration Manager** | System | Manages tuning and calibration profiles for the Master Probability Engine. | AI/ML Team | Validation Metrics | Calibration Profiles | Calibration Profiles | Core Astrological Rules |
| **Validation Framework** | QA/Testing | Executes deterministic test suites against known canonical charts. | QA Team | Test Cases, Engine Outputs | Validation Reports | Validation Reports | Engine Algorithms |
| **Quality Metrics Engine** | QA/Testing | Aggregates and analyzes the statistical accuracy and performance metrics. | QA Team | Validation Reports, Execution Logs | Quality Metrics, Performance Stats | Quality Metrics | Validation Reports |
| **Pipeline Runner** | Infrastructure | Orchestrates the execution graph of all engines. | Platform Team | Execution DAG | Coordinated Execution State | Pipeline State | Business Logic, Astrology Rules |
| **Question Engine** | Orchestrator Only | Question routing, workflow orchestration, and answer composition. (Performs zero astrological calculations). | Backend Team | NLP Intents, Pipeline Outputs | Final Answer Payload | Question Routing, Workflow Orchestration | Deterministic calculations, Engine outputs (must never modify), Pipeline Runner execution (must never bypass). |
| **Mandali Generator** | Canonical Engine | Generates Moon-centered Gochara Transit Boundaries (Mandali spatial grid). | Core Engine Team | Planetary Longitudes, Natal Moon Pada | Mandali Grid, Relative Transit Padas | Mandali Boundaries | Transit Interpretation Logic, Dasha Timing |
| **Transit Engine** | Legacy Reference | Retained ONLY for reusable deterministic logic. NOT the architectural foundation of Version 2. | Core Engine Team | Planetary Positions, Mandali Grid | Legacy Transit Hits | Legacy Transit Calculations | Version 2 Foundation Logic, Final Probabilities |
| **Report Engine** | Presentation | Formats final outputs into human-readable reports and natural language. | Backend Team | Probability Results | Final Formatted Reports | Generated Reports | Astrological Data |
| **API Layer** | Interface | Exposes the system capabilities via standardized REST/GraphQL endpoints. | Backend Team | Client Requests | Structured API Responses | API Responses | Internal State |
| **Frontend** | Interface | Provides the user interface for interactions and viewing reports. | Frontend Team | API Responses, User Inputs | User Interface Views | UI State | Any Astrological Logic |

---

## SECTION 4: Canonical Data Ownership Registry

| Data Object | Canonical Owner | Consumers | Modification Policy |
| :--- | :--- | :--- | :--- |
| **Planet Strength** | Planet Engine | House, Varga, Yoga, Dosha, Functional Nature | Strictly Read-Only for consumers. Only mutable by Planet Engine. |
| **House Strength** | House Engine | Yoga, Dosha, Functional Nature | Strictly Read-Only for consumers. Only mutable by House Engine. |
| **Varga Results** | Varga Engine | Dasha, Yoga, Master Probability | Strictly Read-Only for consumers. Only mutable by Varga Engine. |
| **Dasha Activation** | Dasha Engine | Master Probability, Report Engine | Strictly Read-Only for consumers. Only mutable by Dasha Engine. |
| **Yoga Detection** | Yoga Engine | Master Probability | Strictly Read-Only for consumers. Only mutable by Yoga Engine. |
| **Dosha Detection** | Dosha Engine | Master Probability | Strictly Read-Only for consumers. Only mutable by Dosha Engine. |
| **Functional Nature** | Functional Nature Engine | Master Probability, Yoga, Dosha | Strictly Read-Only for consumers. Only mutable by Functional Nature Engine. |
| **Probability Result** | Master Probability Engine | Report Engine, Quality Metrics Engine | Strictly Read-Only for consumers. Only mutable by Master Probability Engine. |
| **Calibration Profiles** | Calibration Manager | Master Probability Engine | Writable only by Calibration Manager. |
| **Validation Reports** | Validation Framework | Quality Metrics Engine, Calibration Manager | Writable only by Validation Framework. |
| **Quality Metrics** | Quality Metrics Engine | Calibration Manager, Engine Teams | Writable only by Quality Metrics Engine. |
| **Question Routing** | Question Engine | Pipeline Runner, Master Probability Engine | Writable only by Question Engine. |
| **Generated Reports** | Report Engine | API Layer | Writable only by Report Engine. |
| **API Responses** | API Layer | Frontend | Writable only by API Layer. |
| **UI State** | Frontend | User | Writable only by Frontend. |

---

## SECTION 5: Input Contract Principles

* **Immutable Inputs**: Once an input is provided to an engine, it is strictly immutable. No downstream process or engine may modify or overwrite the input data it receives.
* **Explicit Dependencies**: All inputs required by an engine must be explicitly declared in its input contract. Implicit dependencies, back-channel state reads, and global variables are strictly prohibited.
* **Pipeline-Controlled Delivery**: The orchestration of data between engines is the sole responsibility of the Pipeline Runner. Engines must not attempt to fetch data from other engines directly; they must wait for the Pipeline Runner to deliver it.
* **Deterministic Contracts**: Input contracts must be fully deterministic. Given the exact same set of input parameters and state, an engine must always produce the exact same deterministic output.

---

## SECTION 6: Output Contract Principles

* **Ownership of Outputs**: An engine is the sole and exclusive owner of its outputs. No other component in the system is permitted to generate, alter, or redefine those specific outputs.
* **Deterministic Outputs**: Outputs must be 100% deterministic and reproducible. Non-deterministic behaviors, randomness, or time-dependent variations not explicitly passed as inputs are forbidden.
* **Explainable Outputs**: Every output must be explainable. The trace of how an output was derived (the lineage) must be transparent and verifiable by the Validation Framework.
* **Version Compatibility**: Output contracts are versioned. Changes to output schemas require formal version increments and must not break downstream consumers implicitly.
* **No Cross-Engine Modification**: Downstream engines may consume outputs but must never modify them or pass them off as their own derived state.

---

## SECTION 7: Ownership Rules

* **One Owner Per Object**: Every data object, concept, or calculated metric has exactly one authoritative owner.
* **No Duplicated Calculations**: No two engines shall perform the same calculation. If an engine requires a calculation owned by another, it must consume it via the Pipeline Runner.
* **No Ownership Leakage**: An engine must not allow its internal state or unfinalized calculations to leak to other engines. Only formally contracted outputs may be shared.
* **No Hidden Calculations**: All calculations must be explicit, documented, and testable by the Validation Framework.
* **No Implicit Ownership**: Ownership must be explicitly defined in this registry. "Assuming" ownership of a domain is a violation of the architecture.
* **No Circular Ownership**: Dependencies between engines must form a Directed Acyclic Graph (DAG). Circular dependencies and circular data ownership are strictly forbidden.

---

## SECTION 8: Ownership Transfer Policy

The ownership defined in this registry is considered constitutional. Any transfer or modification of ownership requires a formal, rigorous process:

* **Architecture Decision Record (ADR)**: A formal ADR must be authored explaining the rationale, impact, and technical implementation of the ownership change.
* **Architecture Review**: The ADR must be reviewed and approved by the core architecture board.
* **Documentation Update**: This registry and any related architectural documentation must be updated to reflect the approved change.
* **Regression Verification**: The Validation Framework must pass 100% of the regression suite to ensure the ownership change did not introduce deterministic drift.
* **Version Increment**: Ownership transfers represent a major architectural shift and require a formal increment to the system's architectural version.

---

## SECTION 9: Illustrative Examples

* **Example 1**: The **Planet Engine** owns planetary strength (Shadbala). The **House Engine** may consume this strength to calculate certain aspects, but it must never redefine or recalculate planetary strength itself.
* **Example 2**: The **Master Probability Engine** synthesizes all outputs (Yogas, Doshas, Strengths) to generate a final probability score. However, it must never recalculate a Yoga or alter a planet's Functional Nature in order to achieve a specific probability. It only synthesizes; it does not originate astrological data.
* **Example 3**: The **Question Engine** interprets user intent, orchestrates the workflow, and composes the final answer. As an **Orchestrator Only**, it is bound by strict constitutional restrictions: it performs zero astrological calculations, never owns deterministic calculations, never modifies engine outputs, and never bypasses the Pipeline Runner.

---

## SECTION 10: Governance Freeze

This document, the Engine Ownership and Data Contract Registry, is hereby declared part of the permanent Golden Master Constitution.

The architectural boundaries and ownership responsibilities defined within are considered strictly frozen. Future ownership changes, additions of new engines, or modifications to canonical data objects require formal governance approval and adherence to the Ownership Transfer Policy (Section 8).
