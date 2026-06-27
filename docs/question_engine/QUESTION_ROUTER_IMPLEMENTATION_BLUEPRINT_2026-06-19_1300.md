# QUESTION ROUTER IMPLEMENTATION BLUEPRINT

**Date:** 2026-06-19_1300
**Version:** Phase 9 Step 3C

## OBJECTIVE
This document defines the exact routing flow for the Vedic AI Question Engine. It explicitly maps how an input question traverses the system:
**Question → Question ID → Domain → Formula Group → Answer Composer → Timing Engine → Final Answer**

---

## SECTION 1: QUESTION ID SYSTEM

To ensure programmatic stability and decoupled formula execution, all supported questions are assigned a standardized, immutable ID. 

### Naming Conventions
The convention follows a `[DOMAIN_PREFIX]_[XXX]` format.

*   **MLA_001+**: Master Life Analysis
*   **MAR_001+**: Marriage & Relationships
*   **CAR_001+**: Career & Profession
*   **FIN_001+**: Finance & Wealth
*   **PRO_001+**: Property & Vehicles
*   **HEA_001+**: Health & Disease
*   **CHI_001+**: Children & Progeny
*   **EDU_001+**: Education
*   **BUS_001+**: Business & Partnerships
*   **FOR_001+**: Foreign Travel & Settlement
*   **SPI_001+**: Spiritual & Dharma
*   **STR_001+**: Strategic Life Questions
*   **CUS_001+**: Custom NLP Generated Queries

---

## SECTION 2: DOMAIN ROUTER

The Domain Router's primary responsibility is to map the resolved `Question ID` directly to a high-level `Domain`. 

### Domain Mapping Table
| Question ID Prefix | Target Domain |
| :--- | :--- |
| **MLA_** | Master Life Analysis |
| **MAR_** | Marriage |
| **CAR_** | Career |
| **FIN_** | Finance |
| **PRO_** | Property |
| **HEA_** | Health |
| **CHI_** | Children |
| **EDU_** | Education |
| **BUS_** | Business |
| **FOR_** | Foreign |
| **SPI_** | Spiritual |
| **STR_** | Strategic |

---

## SECTION 3: FORMULA GROUP ROUTER

Once a Domain is identified, the router delegates execution to a specific `Formula Group` within the externalized Formula Repository. **(Note: Routing logic only. Formulas are not implemented here).**

### Formula Group Mapping Example
| Question ID | Domain | Formula Group Triggers |
| :--- | :--- | :--- |
| **MAR_001** | Marriage | `Marriage Promise`, `Marriage Timing` |
| **MAR_002** | Marriage | `Spouse Characteristics`, `Marriage Promise` |
| **CAR_001** | Career | `Career Promise`, `Career Timing` |
| **CAR_004** | Career | `Career Change Trigger`, `Career Timing` |
| **FIN_001** | Finance | `Wealth Promise`, `Wealth Timing` |
| **FIN_003** | Finance | `Debt Risk`, `Wealth Timing` |
| **HEA_001** | Health | `Vitality Promise`, `Disease Timing` |

*The Formula Group Router ensures that the engine only executes the mathematical astrology logic necessary to answer the specific query.*

---

## SECTION 4: ANSWER COMPOSER FLOW

As defined in the Phase 9 Step 3A Governance Package, the Answer Composer enforces a strict 5-part synthesis contract for all routed formula evaluations. The Router passes the evaluation payload to the Composer to generate:

1.  **Promise:** (Natal Potential confirmation)
2.  **Strength:** (Quantitative Shadbala/Bhava Bala metrics)
3.  **Reason:** (Astrological logic explanation)
4.  **Timing:** (Chronological manifestation window via Timing Engine)
5.  **Advice:** (Remedial or practical guidance)

---

## SECTION 5: CUSTOM QUESTION ROUTER

When a user enters free text that does not strictly match a predefined ID (e.g., "Should I become a doctor?", "Should I start a hospital in London?"), the Custom Question Router activates.

### Classification Flow
1.  **NLP Intent Parsing:** Determines the core Subject and Action.
    *   *Query:* "Should I settle abroad?"
    *   *Subject:* Foreign Settlement
    *   *Action:* Timing / Promise
2.  **Domain Intersection:** Maps Subject to established Domains.
    *   *Mapping:* `FOR_` (Foreign)
3.  **Dynamic ID Assignment:** Assigns a temporary runtime `CUS_XXX` ID.
4.  **Formula Assembly:** Constructs a dynamic array of Formula Groups (e.g., `Foreign Settlement Promise` + `Career Promise`).
5.  **Execution Pipeline:** Proceeds normally to Answer Composer.

---

## SECTION 6: FALLBACK STRATEGY

To maintain high confidence, the Router employs strict fallback safety nets:

*   **Unknown Question:** If the Custom Router cannot confidently extract a Subject, it immediately halts and requests clarification ("I am unable to determine the astrological parameters for this question. Could you rephrase?").
*   **Multi-Domain Question:** If a query spans >2 unrelated domains (e.g., "Will I get married and become a billionaire?"), the Router isolates and processes the primary domain first, queueing the secondary domain as a follow-up.
*   **Ambiguous Question:** Defaults to Master Life Analysis (`MLA_001` - General Life Promise) if intent is purely exploratory.
*   **Future NLP Expansion:** The router is decoupled so that future LLM parsers can simply return standard `Question IDs` to the Python engine.

---

## SECTION 7: FUTURE INTEGRATION POINTS

The routing architecture is designed with clear interception hooks for subsequent deployment phases:

1.  **LLM Layer:** Future OpenAI/Gemini integration will act solely as the NLP parser for Section 5 (Custom Router), translating raw text to `Question IDs` and `Formula Groups`.
2.  **Gochara Layer:** Transit modifiers will intercept between the Formula Router and Timing Engine.
3.  **Ashtakavarga Layer:** SAV/BAV thresholds will act as a gating mechanism for the Formula Group execution.
4.  **Mandali Transit Layer:** Moon-centric transit conditions will modify the severity of the `Strength` output in the Answer Composer.
5.  **Future AI Ranking Layer:** A machine learning model to prioritize which `Formula Group` carries the most weight based on statistical probability.
