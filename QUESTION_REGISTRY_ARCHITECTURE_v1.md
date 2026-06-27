# QUESTION REGISTRY ARCHITECTURE v1

## 1. System Objective
Transition the Vedic AI System's Question Engine from a purely free-text, LLM-based intent parser to a deterministic **Question Registry Framework**. This framework organizes queries hierarchically, anchoring every astrological question to a specific `question_id` that maps to precise mathematical requirements.

## 2. Structural Hierarchy
The framework is organized into the following cascading structure:

1. **24 Master Domains** (Derived from 12 Houses and their primary significations)
2. **200+ Child Questions** (Granular, specific life events and scenarios)
3. **Question IDs** (Deterministic mathematical mapping keys)
4. **Free-Text Fallback** (NLP resolution when direct IDs are absent)

---

## 3. Input Resolution Modes

The engine will support three input resolution modes to guarantee a match against the Question Registry:

- **Mode A (Direct ID Injection):** The user explicitly selects a predefined question from the UI (e.g., `7.2`). The request payload inherently includes `question_id=MAR_TIMING_001`.
- **Mode B (Natural Language Mapping):** The user types a fully formed question (e.g., "When will marriage happen?"). The NLP router matches the semantic intent to the closest Question ID before execution.
- **Mode C (Typo/Fuzzy Mapping):** The user types fragmented or misspelled keywords (e.g., "marrage"). The system utilizes fuzzy matching or embeddings to snap to the parent Domain and relevant Question IDs.

---

## 4. Question Registry Schema Definition

Every child question in the registry MUST define the following configuration schema to inform the internal astrological engines of the evaluation criteria:

```yaml
question_id: string
domain: string
subdomain: string
required_house_focus: list[int]
required_planets: list[string]
required_yogas: list[string]
required_dasha_check: boolean
required_transit_check: boolean # (future)
required_ashtakavarga_check: boolean
```

### 4.1 Sample Registry Entries

**Marriage Timing**
```yaml
question_id: MAR_TIMING_001
domain: marriage
subdomain: timing
required_house_focus: [7, 2, 11]
required_planets: ["venus", "jupiter"]
required_yogas: ["vivaha_yoga"]
required_dasha_check: true
required_transit_check: true
required_ashtakavarga_check: true
```

**Foreign Career / Relocation**
```yaml
question_id: CAR_FOREIGN_001
domain: career
subdomain: foreign_travel
required_house_focus: [9, 10, 12]
required_planets: ["rahu", "moon"]
required_yogas: ["videsh_vas_yoga"]
required_dasha_check: true
required_transit_check: false
required_ashtakavarga_check: false
```

---

## 5. Timing Governance

For any Question ID where `required_dasha_check` or `subdomain == "timing"` is true, the engine MUST strictly adhere to the following composition:

**Required Active Layers:**
1. **Natal Promise:** Baseline probability for the event.
2. **Mahadasha (MD):** Broad activation window.
3. **Antardasha (AD):** Primary timing trigger.
4. **Pratyantardasha (PD):** Precision timing trigger.

**Future Timing Integration:**
- **Mandali Transit Engine:** Real-time planetary transits overlaying the natal chart.
- **Ashtakavarga Timing Layer:** Kakshya-based transit confidence modifiers.

---

## 6. User Experience & UI Blueprint

The front-end Question Panel will be overhauled from a simple text box to a comprehensive **Question Browser UI**.

### 6.1 Layout Elements
- **Search Box:** For dynamic filtering of the 200+ child questions.
- **Question ID Selector:** For advanced users wanting direct ID routing.
- **Recent Questions:** Historical list of asked questions.
- **Favorites:** Saved queries for repeated execution.
- **Collapsible Browser:** Accordion-style navigation grouped by House/Domain.

### 6.2 Collapsible UI Domain Structure (Examples)

**1. Self / Personality (1st House)**
**2. Wealth / Family (2nd House)**
**3. Courage / Communication (3rd House)**
**4. Property / Education (4th House)**
**5. Children (5th House)**
**6. Health (6th House)**

**7. Marriage (7th House)**
- 7.1 Marriage Prospects
- 7.2 Marriage Timing
- 7.3 Delay in Marriage
- 7.4 Love Marriage
- 7.5 Arranged Marriage
- 7.6 Second Marriage
- 7.7 Married Life
- 7.8 Divorce Risk
- 7.9 Spouse Nature
- 7.10 Spouse Profession

**8. Longevity (8th House)**
**9. Fortune (9th House)**

**10. Career (10th House)**
- 10.1 Career Growth
- 10.2 Job Change
- 10.3 Promotion
- 10.4 Government Job
- 10.5 Business
- 10.6 Foreign Career
- 10.7 Self Employment
- 10.8 Career Stability

**11. Gains (11th House)**
**12. Losses / Spirituality (12th House)**
