# KNOWLEDGE_GRAPH_PRODUCT_SPECIFICATION_v1.0.md

# Knowledge Graph Product Specification — Version 1.0

**Status**: Canonical Specification  
**Owner**: Chief Architect  
**Version**: 1.0  
**Date**: 2026-07-27  
**Classification**: Product Specification — Do Not Modify Code

---

## PART 1: PURPOSE OF THE KNOWLEDGE GRAPH

### 1.1 Why Does the Knowledge Graph Exist?

The Knowledge Graph exists to **make deterministic astrological intelligence traceable, navigable, and explainable**.

In Vedic Astrology, every prediction rests on a chain of deterministic calculations:
- Planetary positions → Dignity scores → House strengths → Domain promises → Transit triggers → Dasha timing → Master probability

Today, this chain is invisible. A consultant sees "Marriage: 61/100" but cannot answer:
- *Which formula produced this?*
- *Which calibration constant was applied?*
- *Which transit is activating this domain right now?*
- *What would change the score by 10 points?*

The Knowledge Graph makes the **entire reasoning chain visible, navigable, and verifiable**.

### 1.2 User Problems Solved

| User | Problem | Graph Solution |
|------|---------|----------------|
| **Astrology Expert** | "Why does this chart show weak marriage?" | Trace from domain → house → planet → dignity → formula → calibration |
| **Consultant** | "Explain the transit trigger to my client" | Show Gochara Mandali → current transit positions → activated domains |
| **AI Assistant** | "Why did you recommend this timing?" | Trace prediction → probability factors → transit triggers → dasha sync |
| **Formula Verifier** | "Is the dignity score correct?" | Formula → calibration constants → planetary inputs |
| **Report Auditor** | "Trace this prediction to source" | Consultation → question → domain → natal promise → transit → dasha |

### 1.3 Non-Goals

- NOT a general-purpose graph database
- NOT a user-editable wiki
- NOT an AI training corpus
- NOT a replacement for deterministic engines

---

## PART 2: NODE TYPE SPECIFICATIONS

### 2.1 Planet Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `planet` |
| **Examples** | Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu |
| **Description** | "Sun — Planet: Soul, authority, father, government. Dignity evaluated from sign placement." |
| **Purpose** | Core astrological actors; inputs to all planet-strength formulas |
| **Properties** | `significance` (string), `natural_benefic` (boolean), `natural_malefic` (boolean), `exaltation_sign` (string), `debilitation_sign` (string), `own_signs` (string[]) |
| **Relationships** | `influences` → Formula (Dignity Score), `occupies` → House, `aspects` → Planet, `triggers` → Transit |
| **Evidence** | Planetary position from Canonical JSON; dignity from sign placement |
| **References** | Classical texts: BPHS Ch. 3, Saravali Ch. 3 |
| **Related Formulas** | PLN-DG-001 (Dignity Score), PLN-HP-001 (House Placement), PRB-AG-001 (Probability Aggregation) |
| **Related Reports** | Planet Strength Report, Natal Promise Domain Scores |
| **Related Engines** | PlanetStrengthEngine, TransitEngine, NatalPromiseEngine |
| **Related Consultations** | All domain questions involving planetary strength |
| **Related Questions** | Q1.1 (Planet Strength), Q7.1 (Planet Dignity) |
| **Related Calculations** | Dignity score (20/40/50/60/80/100), House placement score, Aspect strength |

---

### 2.2 House Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `house` |
| **Examples** | House 1 (Lagna), House 7 (Kalatra), House 10 (Karma) |
| **Description** | "House 7 — Kalatra: Marriage, partnerships, business contracts. Governed by 7th lord." |
| **Purpose** | Life domains; domain promise calculation; transit house activation |
| **Properties** | `house_number` (1-12), `bhava_name` (string), `lord_planet` (string), `bhava_type` (Kendra/Trikona/Dusthana/Neutral), `significance` (string) |
| **Relationships** | `contains` → Planet (occupancy), `lorded_by` → Planet (lordship), `activates` → Transit, `maps_to` → Domain |
| **Evidence** | House cusp from Canonical JSON; lord from planetary rulership |
| **References** | BPHS Ch. 13-16, Jataka Parijata Ch. 2 |
| **Related Formulas** | TRN-HA-001 (House Activation), PLN-HP-001 (House Placement), Natal Promise per domain |
| **Related Reports** | House Strength Report, Domain Promise Report |
| **Related Engines** | HouseStrengthEngine, TransitEngine, NatalPromiseEngine |
| **Related Consultations** | Domain-specific questions (Marriage→H7, Career→H10, Wealth→H2/H11) |
| **Related Questions** | Q2.1 (House Strength), Q3.1 (House Occupancy) |
| **Related Calculations** | House activation score, Bhava Bala, Lord strength |

---

### 2.3 Transit Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `transit` |
| **Examples** | Transit Activation, Sadesati, Ashtam Shani, Jupiter Return |
| **Description** | "Transit Activation: Overall transit activation score (0-100) from 5 subsystems." |
| **Purpose** | Current planetary positions → domain activation scores |
| **Properties** | `has_subsystems` (boolean), `planet` (string), `duration` (string), `period` (number), `subsystems` (string[]) |
| **Relationships** | `explains` ← Formula (TRN-HA-001, TRN-BV-001, TRN-PA-001, TRN-DS-001, TRN-VD-001), `triggers` → Domain activation, `timed_by` → Dasha |
| **Evidence** | Current planetary positions from Canonical JSON current_transit; house_from_moon |
| **References** | BPHS Gochara Ch. 1-3, Phaladeepika Ch. 19 |
| **Related Formulas** | TRN-HA-001, TRN-BV-001, TRN-PA-001, TRN-DS-001, TRN-VD-001 |
| **Related Reports** | Transit Report, Gochara Mandali Advisory, Lifetime Cycle Projection |
| **Related Engines** | TransitEngine, UniversalMandaliEngine, LifetimeCycleProjector |
| **Related Consultations** | Timing questions, Sadesati analysis, Transit timing |
| **Related Questions** | Q10.1 (Transit Timing), Q10.2 (Sadesati Status) |
| **Related Calculations** | House activation, BAV support, Planet activation, Dasha sync, Vedha layer |

---

### 2.4 Gochara Mandali Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `concept` (specialized: `gochara_mandali`) |
| **Examples** | Gochara Mandali (Current), Mandali 1–12 |
| **Description** | "Gochara Mandali: Moon-centered 12-mandali grid resolving current transit positions to mandali numbers for precise gochara analysis." |
| **Purpose** | Moon-centered spatial reference frame for transit resolution per Capability 7.1–7.7 |
| **Properties** | `mandali_number` (1-12), `center_nakshatra` (string), `center_pada` (int), `reference_moon_nakshatra` (string), `reference_moon_pada` (int), `current_transit_mandali` (object per planet) |
| **Relationships** | `resolves` → Transit (planet positions), `centered_on` → Moon (nakshatra/pada), `generates` → Mandali Advisory, `activates` → Sadesati/Elinati/Ashtama |
| **Evidence** | Moon nakshatra/pada from Canonical JSON; transit positions from current_transit; canonical reference data registries |
| **References** | GOCHARA_MANDALI_GOVERNANCE_v1.md, BPHS Gochara |
| **Related Formulas** | Mandali grid construction (MGC-01 to MGC-07), Transit resolution (TMR-01 to TMR-05) |
| **Related Reports** | Gochara Mandali Advisory, Mandali Activations, Sadesati/Elinati/Ashtama windows |
| **Related Engines** | UniversalMandaliEngine, MandaliGridConstruction, TransitMandaliResolution, NakshatraPadaResolver, LifetimeCycleProjector |
| **Related Consultations** | Sadesati analysis, Mandali timing, Transit precision |
| **Related Questions** | Q10.3 (Mandali Position), Q10.4 (Sadesati Phase) |
| **Related Calculations** | Moon absolute pada, Transit absolute pada, Mandali assignment, Cycle projection |

---

### 2.5 Mandali Node (Individual Mandali 1-12)

| Attribute | Specification |
|-----------|---------------|
| **Type** | `mandali` |
| **Examples** | Mandali 1 (Krittika center), Mandali 9 (Uttara Ashadha center) |
| **Description** | "Mandali 9: Center=Uttara Ashadha Pada 1, Rasi=Makara. Contains 9 padas from Uttara Phalguni P4 to Shravana P2." |
| **Purpose** | Spatial reference frame unit; 9-pada window centered on nakshatra pada |
| **Properties** | `number` (1-12), `center_pada` (1-108), `center_nakshatra` (string), `center_pada_num` (1-4), `rasi_name` (string), `padas` (int[9]), `pada_details` (object[]) |
| **Relationships** | `contains` → Transit (planet position), `centered_on` → Nakshatra Pada, `belongs_to` → Gochara Mandali |
| **Evidence** | Nakshatra-Pada Registry (108 entries), Rasi mapping |
| **Related Formulas** | MGC-01 to MGC-07 (Mandali Grid Construction) |
| **Related Reports** | Current Mandali, Mandali Activations, Transit Mandali Resolution |
| **Related Engines** | MandaliGridConstruction, TransitMandaliResolution |

---

### 2.6 Formula Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `formula` |
| **Examples** | "House Activation (TRN-HA-001)", "Dignity Score (PLN-DG-001)", "Probability Aggregation (PRB-AG-001)" |
| **Description** | "House Activation (TRN-HA-001): 30% weight — Measures house activation from transit planets using classical gochara quality matrix." |
| **Purpose** | Deterministic calculation rules; traceable to calibration constants |
| **Properties** | `formula_id` (string), `domain` (transit/planet/probability/dasha/yoga), `weight` (number), `subsystems` (string[]), `inputs` (string[]), `output` (string) |
| **Relationships** | `depends_on` → Calibration (5 per formula), `explains` → Transit/Domain, `used_in` → Engine, `validated_by` → Governance |
| **Evidence** | Formula registry (YAML), Calibration constants, Engine implementation |
| **References** | Formula Registry (YAML), AP-003 System Governance |
| **Related Formulas** | Depends on 5 calibrations; explains transit subsystems |
| **Related Reports** | Formula Evaluation Report, Subsystem Breakdown |
| **Related Engines** | TransitEngine, PlanetStrengthEngine, MasterProbabilityEngine |
| **Related Consultations** | All — every consultation uses formulas |
| **Related Questions** | All formula-related questions |
| **Related Calculations** | Per formula specification |

---

### 2.7 Calibration Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `calibration` |
| **Examples** | "Own Sign (80)", "Friendly Sign (60)", "Neutral (50)", "Enemy (40)", "Debilitated (20)" |
| **Description** | "Own Sign: Planet in its own sign gets 80% strength. Constant used by Dignity Score formula." |
| **Purpose** | Immutable constants; versioned; governance-controlled |
| **Properties** | `constant_id` (string), `value` (number), `unit` (string), `description` (string), `governance_doc` (string) |
| **Relationships** | `calibrated_by` ← Formula (5 per formula), `validated_by` → Governance |
| **Evidence** | Calibration Registry (YAML), AP-003 Governance |
| **References** | Calibration Registry (YAML), AP-003 |
| **Related Formulas** | PLN-DG-001, PLN-HP-001, TRN-PA-001, TRN-DS-001, etc. |
| **Related Reports** | Calibration Audit, Formula Evaluation |
| **Related Engines** | PlanetStrengthEngine, TransitEngine, MasterProbabilityEngine |
| **Related Consultations** | Formula verification, Calibration audit |

---

### 2.8 Yoga Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `yoga` |
| **Examples** | "Gaja Kesari Yoga", "Raja Yoga", "Dhana Yoga", "Moksha Yoga", "Ruchaka Yoga" |
| **Description** | "Gaja Kesari Yoga: Jupiter in Kendra from Moon. Bestows wisdom, wealth, royal status." |
| **Purpose** | Classical planetary combinations; qualitative modifiers |
| **Properties** | `yoga_name` (string), `classical_type` (string), `strength` (number), `planets_involved` (string[]), `houses_involved` (int[]) |
| **Relationships** | `detected_by` ← YogaEngine, `modifies` → Planet/Domain, `appears_in` → Report |
| **Evidence** | Planetary positions from Canonical JSON; classical rules |
| **References** | BPHS Ch. 41-44, Phaladeepika Ch. 6-7 |
| **Related Formulas** | YOG-DT-001 (Yoga Detection), Domain promise modifiers |
| **Related Reports** | Yoga Report, Natal Promise modifiers |
| **Related Engines** | YogaEngine, NatalPromiseEngine |
| **Related Consultations** | Yoga analysis, Raja Yoga timing |

---

### 2.9 Dasha Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `dasha` |
| **Examples** | "Saturn Mahadasha", "Jupiter Antardasha", "Mercury Pratyantardasha" |
| **Description** | "Saturn Mahadasha: 19-year period. Active 2020-2039. Current AD: Jupiter (2024-2026)." |
| **Purpose** | Vimshottari timing; activates transit-domain synchronization |
| **Properties** | `dasha_level` (MD/AD/PD), `lord` (string), `start_date` (string), `end_date` (string), `duration_years` (number), `system` (string: "Vimshottari") |
| **Relationships** | `times` → Transit Sync, `activates` → Domain, `governed_by` → Planet (lord), `contains` → Antardasha |
| **Evidence** | Vimshottari calculation from birth data; Canonical JSON dasha timeline |
| **References** | BPHS Ch. 45-48, Phaladeepika Ch. 14 |
| **Related Formulas** | TRN-DS-001 (Dasha Sync), DSH-PR-001 (Dasha Period) |
| **Related Reports** | Dasha Report, Dasha-Transit Sync, Lifetime Cycle Projection |
| **Related Engines** | DashaEngine, TransitEngine, LifetimeCycleProjector |
| **Related Consultations** | Timing questions, Mahadasha analysis, Antardasha prediction |

---

### 2.10 Governance Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `governance` |
| **Examples** | "AI Governance (AP-002)", "System Governance (AP-003)", "GM-007 Freeze" |
| **Description** | "System Governance (AP-003): Platform-wide governance rules. Constitution for deterministic engines." |
| **Purpose** | Immutable rules; version control; freeze enforcement |
| **Properties** | `document_id` (string), `version` (string), `status` (FROZEN/ACTIVE/ARCHIVED), `scope` (string) |
| **Relationships** | `supersedes` → AI Governance, `validated_by` → Freeze, `governs` → Engine/Formula/Calibration |
| **Evidence** | Governance documents (AP-001 through AP-004), GM-007 Freeze Declaration |
| **References** | AP-001 through AP-004, GM-007 Freeze Declaration |
| **Related Reports** | Governance Audit, Freeze Compliance |
| **Related Engines** | All engines (governance compliance check) |

---

### 2.11 Probability Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `probability` |
| **Examples** | "Master Probability (Marriage: 61/100)", "Marriage Domain Score" |
| **Description** | "Marriage: 61/100 (MODERATE). Natal Promise: 45, Transit: 78, Dasha: 65." |
| **Purpose** | Final synthesized output; weighted synthesis |
| **Properties** | `final_score` (0-100), `grade` (string), `breakdown` (object), `weights` (object), `stub_factors` (string[]) |
| **Relationships** | `aggregates` ← Natal Promise/Planet/House/Rasi/Varga/Dasha/Transit, `used_in` → Report/Question |
| **Evidence** | Engine outputs, weights from Calibration |
| **References** | Master Probability Engine, AP-003 Governance |
| **Related Reports** | Master Probability Report, Question Answer, Consultation Report |
| **Related Engines** | MasterProbabilityEngine, QuestionEngine |
| **Related Consultations** | All — final output for every question |

---

### 2.12 Concept Node

| Attribute | Specification |
|-----------|---------------|
| **Type** | `concept` |
| **Examples** | "Gochara Mandali", "Sadesati", "Ashtam Shani", "Kendra", "Trikona", "Dusthana" |
| **Description** | "Gochara Mandali: Moon-centered 12-mandali grid for transit resolution per Capability 7.1–7.7." |
| **Purpose** | High-level concepts; teaching; cross-domain linking |
| **Properties** | `concept_type` (string), `definition` (string), `related_terms` (string[]) |
| **Relationships** | `explains` → Node, `instantiates` → Instance, `categorizes` → Domain |
| **Evidence** | Classical definitions, Governance documents |
| **References** | Classical texts, Governance documents |
| **Related Reports** | Educational, Glossary |

---

## PART 3: RELATIONSHIP TYPES

| Relationship | Direction | Meaning | Example | Evidence Required |
|--------------|-----------|---------|---------|-------------------|
| `depends_on` | Formula → Calibration | Formula requires calibration constant | TRN-HA-001 → Own Sign (80) | Calibration registry entry |
| `explains` | Formula → Transit/Domain | Formula contributes to subsystem | TRN-HA-001 → Transit Activation | Formula registry weight |
| `influences` | A → B | A modifies B's score/behavior | Dignity Score → Sun (Planet) | Formula logic trace |
| `explains` | Formula → Engine Output | Formula explains engine output | TRN-HA-001 → Transit Activation | Formula weight in engine |
| `uses` | Engine → Formula | Engine consumes formula | TransitEngine → TRN-HA-001 | Engine source code |
| `produces` | Engine → Node | Engine generates node | PlanetStrengthEngine → Sun (planet) | Engine output |
| `affects` | Transit → Domain | Transit activates domain | Saturn transit → Marriage domain | TransitEngine calculation |
| `strengthens` | A → B | A increases B's score | Jupiter transit → Wealth domain | Transit quality matrix |
| `weakens` | A → B | A decreases B's score | Saturn transit → Marriage domain | Transit quality matrix |
| `references` | House → Planet | Planet may occupy house | House 7 → Venus | House lordship |
| `calibrated_by` | Formula → Calibration | Formula uses calibration | Dignity Score → Own Sign | Calibration registry |
| `triggered_by` | Event → Transit | Transit triggers event | Saturn transit → Sadesati | Transit position |
| `used_in` | Formula → Engine | Formula used in engine | PRB-AG-001 → MasterProbabilityEngine | Engine source |
| `appears_in_report` | Node → Report | Node appears in report | Saturn → Sadesati Report | Report template |
| `asked_by_question` | Question → Node | Question queries node | "Will I marry?" → Marriage domain | Question registry |
| `used_by_engine` | Node → Engine | Node consumed by engine | Sun (planet) → PlanetStrengthEngine | Engine input schema |
| `derived_from` | Node → Formula | Node derived from formula | Transit Activation → TRN-HA-001 | Formula lineage |
| `validated_by` | Freeze → Governance | Freeze validates governance | GM-007 Freeze → System Governance | Freeze declaration |
| `supersedes` | Governance → Governance | Higher governance supersedes | System Governance → AI Governance | Governance hierarchy |
| `validated_by` | Freeze → Governance | Freeze validates governance | GM-007 Freeze → System Governance | Freeze declaration |
| `explains` | Formula → Transit | Formula explains transit subsystem | TRN-HA-001 → Transit Activation | Formula weight |
| `produces` | Engine → Node | Engine produces node | UniversalMandaliEngine → Gochara Mandali | Engine output |

---

## PART 4: EVIDENCE LEVELS

### 4.1 Evidence Hierarchy (Highest to Lowest)

| Level | Type | Description | Example |
|-------|------|-------------|---------|
| **L1** | **Canonical Rule** | Immutable rule from governance/classical text | "Own Sign = 80" (Calibration Registry) |
| **L2** | **Formula** | Deterministic calculation rule | "House Activation = Σ(quality) + 50" |
| **L3** | **Calibration** | Immutable constant from registry | "Own Sign = 80" (Calibration Registry v1.0) |
| **L4** | **Engine Output** | Deterministic engine computation | "Sun Dignity = 80 (Own Sign)" |
| **L5** | **Canonical Data** | Canonical JSON input | "Sun in Leo (Own Sign)" |
| **L6** | **Engine Output (Derived)** | Derived engine output | "Transit Activation = 72" |
| **L7** | **Classical Text** | Classical reference | "BPHS Ch. 3: Sun in Leo = Own Sign" |
| **L8** | **Expert Rule** | Documented expert heuristic | "Saturn in 7th delays marriage" |
| **L9** | **ADR** | Architecture Decision Record | "ADR-004: Mandali uses Moon-centered frame" |
| **L10** | **Version** | Version metadata | "Formula Registry v1.2" |

### 4.2 Evidence Display Per Node

Every node in the UI must show:

| Field | Source | Display |
|-------|--------|---------|
| **Evidence Summary** | Highest-level evidence on node | "Calibration: Own Sign=80 (L2)" |
| **Evidence Chain** | Chain from node to canonical rules | Formula → Calibration → Canonical Rule |
| **Confidence** | 0-100 based on evidence level | L1=100, L2=90, L3=80, L4=70, L5=60, L6=50, L7=40, L8=30, L9=20, L10=10 |
| **Source** | Primary source document | "Calibration Registry v1.0" |
| **Revision** | Version/timestamp | "v1.0 (2026-01-15)" |
| **Traceability** | Full chain to canonical | Node → Formula → Calibration → Registry |

---

## PART 5: USER EXPERIENCE

### 5.1 Click Behavior Specification

| Click Target | Navigation | Detail Panel Shows |
|--------------|------------|-------------------|
| **Sun** | Planet detail | Dignity: 80 (Own Sign), House: 1, Aspects: [Saturn], Transit: Leo, Evidence: L2 Calibration |
| **Moon** | Planet detail | Dignity: 50 (Neutral), House: 2, Sadesati: Rising (Makara), Evidence: L2 Calibration |
| **Mars** | Planet detail | Dignity: 60 (Own Sign), House: 8, Aspects: [Sun], Transit: Capricorn, Evidence: L2 |
| **House 7** | House detail | Lord: Venus, Occupants: [Saturn], Domain: Marriage, Transit: Saturn→H7, Evidence: L4 |
| **Transit Activation** | Transit detail | Score: 72, Subsystems: [HA:68, BV:75, PA:70, DS:65, VD:60], Evidence: L4 |
| **Gochara Mandali** | Mandali detail | Current: Mandali 9 (Uttara Ashadha), Moon: Krittika P1, Transits: [Jupiter→M1, Saturn→M9], Evidence: L4 |
| **Dignity Formula** | Formula detail | PLN-DG-001: inputs=[planet, sign], output=dignity(0-100), deps=[5 calibrations], Evidence: L2 |
| **Question 32** | Question detail | "Will I get married?", Domain=Marriage, Formula=MAR-DEL, Domain=Marriage, Evidence: L3 |
| **Consultation Report** | Report view | Native: Raju, Score: 61, Breakdown: [Natal:45, Transit:78, Dasha:65], Evidence: L3 |
| **Dignity Formula** | Formula detail | Inputs: planet, sign; Output: 0-100; Deps: [Own=80, Friendly=60, Neutral=50, Enemy=40, Debilitated=20] |

### 5.2 Navigation Rules

| Current View | Click | New View |
|--------------|-------|----------|
| Node list | Node | Node detail (right panel) |
| Node detail | Relationship pill | Target node detail |
| Node detail | Evidence tab | Evidence chain (vertical timeline) |
| Node detail | References tab | Cross-reference graph |
| Evidence chain step | Relationship | Relationship detail |
| Evidence chain step | Source node | Source node detail |
| Cross-reference | Related node | Related node detail |
| Formula node | Calibration pill | Calibration detail |
| Formula node | Engine pill | Engine detail |
| Question node | Formula pill | Formula detail |
| Report | Node pill | Node detail |

---

## PART 6: AI INTEGRATION

### 6.1 AI Assistant Capabilities

| Capability | Graph Operation | Output |
|------------|-----------------|--------|
| **Explain Formula** | Traverse `depends_on` from Formula → Calibrations | "TRN-HA-001 uses 5 calibrations: Own Sign (80), Friendly (60)..." |
| **Answer Question** | Traverse Question → Domain → Natal Promise → Transit → Dasha | "Marriage: 61/100. Natal Promise 45, Transit 78 (Jupiter in H9), Dasha 65 (Saturn MD/Jupiter AD)" |
| **Trace Prediction** | Backtrack from Master Probability → Breakdown → Engines → Formulas → Calibrations | "Score 61: Natal Promise 45 (40%), Planet 52 (15%), House 48 (10%), Rasi 55 (10%), Varga 50 (10%), Dasha 65 (10%), Transit 78 (5%)" |
| **Show Reasoning Chain** | Build evidence chain from Formula → Calibrations → Canonical Rules | "TRN-HA-001 weight 30% → depends on 5 calibrations → Own Sign=80 (Calibration Registry v1.0)" |
| **Explain Recommendation** | Trace Recommendation → Question → Domain → Factors | "Recommendation: Wait for Jupiter transit in H9. Current Saturn MD/Jupiter AD favors marriage timing." |
| **Verify Formula** | Traverse Formula → Calibrations → Registry | "PLN-DG-001 Dignity Score uses 5 calibrations from Calibration Registry v1.0" |
| **Trace Prediction to Source** | Consultation → Question → Domain → Engine → Formula → Calibration → Canonical | Full trace from "Marriage: 61" to "BPHS Ch. 3: Sun in Leo = Own Sign" |

### 6.2 AI Query Patterns

| AI Query | Graph Query | Result |
|----------|-------------|--------|
| "Why is marriage score 61?" | `MATCH (q:Question {id:'Q2.1'})-[:asks_by_question]->(d:Domain {name:'Marriage'})<-[:aggregates]-(p:Probability) RETURN p.breakdown` | Breakdown object |
| "What formulas affect transit?" | `MATCH (f:Formula)-[:explains]->(t:Transit) RETURN f` | 5 transit formulas |
| "Trace Sun's dignity" | `MATCH (p:Planet {label:'Sun'})-[:influences]-(f:Formula)-[:depends_on]->(c:Calibration) RETURN f, c` | Dignity formula + 5 calibrations |

---

## PART 7: GAP ANALYSIS

| Gap | Current | Desired | Classification |
|-----|---------|---------|----------------|
| **Node.evidence field missing** | Not in schema/API | Node shows evidence summary | **Critical** |
| **Node.references field missing** | Not in schema/API | Node shows cross-ref count | **Critical** |
| **Node.relationships field missing** | Not in schema/API | Node shows relationship summary | **Critical** |
| **Gochara Mandali isolated** | 0 relationships | Connected to Moon, Transits, Mandalis | **Critical** |
| **Formula→Calibration evidence chain incomplete** | Only `depends_on` used | Full chain: Formula→Calibration→Registry | **High** |
| **Evidence chain requires `derived_from`/`validated_by`** | Seed uses `depends_on`/`explains`/`influences` | Add `derived_from`/`validated_by` types | **High** |
| **Node.evidence field in API response** | Not serialized | Include computed evidence summary | **High** |
| **Node.references field in API response** | Not serialized | Include cross-ref count | **High** |
| **Node.relationships field in API response** | Not serialized | Include relationship summary | **High** |
| **Gochara Mandali relationships missing** | 0 relationships | Connect to Moon, Transits, Mandalis, Sadesati | **High** |
| **Evidence chain requires specific rel types** | Only `derived_from`/`depends_on`/`validated_by` | Map `depends_on`→evidence chain | **Medium** |
| **Frontend evidence tab shows 0 for isolated nodes** | Shows "No evidence chain" | Show "Node isolated — no evidence chain available" | **Medium** |
| **Cross-references tab empty for isolated nodes** | Shows "No cross-references" | Show "Node isolated — no cross-references" | **Medium** |
| **Evidence chain uses only 3 rel types** | `derived_from`, `depends_on`, `validated_by` | Support `explains`, `influences`, `depends_on` | **Medium** |
| **Cross-reference relevance weights** | Only weight-based | Add semantic relevance | **Low** |
| **Evidence chain visual timeline** | Basic list | Vertical timeline with connectors | **Low** |
| **Graph visualization** | List-based | Interactive graph view | **Low** |
| **Node version history UI** | Not displayed | Show version timeline | **Low** |
| **AI citation format** | Basic `[prefix:label vX]` | Rich citation with evidence level | **Low** |

---

## PART 8: BACKLOG

### BL-001: Add Computed Fields to KnowledgeNode Schema
- **Purpose**: Enable frontend to display evidence, references, relationships on nodes
- **Scope**: Add `evidence`, `references`, `relationships` computed fields to `KnowledgeNode` schema; serialize in API
- **Dependencies**: Schema change (`schemas/knowledge.py`), API endpoint (`knowledge.py`), KnowledgeStore computed properties
- **Priority**: Critical
- **Effort**: 3 days
- **Acceptance**: Node API response includes `evidence`, `references`, `relationships` fields; frontend displays counts > 0

### BL-002: Connect Gochara Mandali Node in Seed Data
- **Purpose**: Integrate Gochara Mandali into knowledge graph
- **Scope**: Add relationships in `seed_default_data()`: Moon → Mandali, Mandali → Mandali 1-12, Mandali → Transits, Mandali → Sadesati/Elinati/Ashtama
- **Dependencies**: BL-001 (node fields), seed_default_data() in knowledge_store.py
- **Priority**: Critical
- **Effort**: 2 days
- **Acceptance**: Gochara Mandali node has ≥5 relationships; evidence chain returns steps; cross-references > 0

### BL-003: Add Computed Fields to KnowledgeStore
- **Purpose**: Compute evidence, references, relationships on nodes server-side
- **Scope**: Add `get_node_evidence()`, `get_node_references()`, `get_node_relationships()` methods; include in `list_nodes()`/`get_node()` serialization
- **Dependencies**: BL-001 (schema)
- **Priority**: Critical
- **Effort**: 3 days
- **Acceptance**: `/nodes` and `/state` return nodes with `evidence`, `references`, `relationships` fields populated

### BL-004: Map Seed Relationship Types to Evidence Chain
- **Purpose**: Enable evidence chains for existing seed relationship types
- **Scope**: Update `buildEvidenceChain()` in frontend and `build_evidence_chain()` in backend to support `depends_on`, `explains`, `influences`, `explains` in addition to `derived_from`/`validated_by`
- **Dependencies**: BL-002 (Gochara Mandali connections)
- **Priority**: High
- **Effort**: 2 days
- **Acceptance**: Evidence chain returns steps for Formula→Calibration (`depends_on`), Formula→Transit (`explains`), Calibration→Formula (`influences`)

### BL-005: Add Computed Fields to API Response
- **Purpose**: Serialize computed fields in API responses
- **Scope**: Update `KnowledgeNode` Pydantic model with computed fields; ensure `/nodes`, `/nodes/{id}`, `/state` include new fields
- **Dependencies**: BL-003
- **Priority**: Critical
- **Effort**: 1 day
- **Acceptance**: API responses include `evidence`, `references`, `relationships` on every node

### BL-006: Update Frontend Node Display
- **Purpose**: Show evidence, references, relationships counts on node list/detail
- **Scope**: Update `KnowledgeGraphViewer.tsx` to use `node.evidence`, `node.references`, `node.relationships` from API; fallback to client-side computation
- **Dependencies**: BL-005
- **Priority**: Critical
- **Effort**: 2 days
- **Acceptance**: Node list shows evidence/ref/rel counts > 0; detail panel shows counts

### BL-007: Evidence Chain Relationship Type Mapping
- **Purpose**: Support all seed relationship types in evidence chain
- **Scope**: Map `depends_on`→evidence, `explains`→evidence, `influences`→evidence, `explains`→evidence in both frontend and backend chain builders
- **Dependencies**: BL-004
- **Priority**: High
- **Effort**: 2 days
- **Acceptance**: Evidence chain returns steps for all formula/calibration/transit relationships

### BL-008: Cross-Reference Relevance Enhancement
- **Purpose**: Improve cross-reference relevance classification
- **Scope**: Add semantic relevance (domain overlap, formula shared, planet shared) beyond weight-based
- **Dependencies**: BL-003
- **Priority**: Medium
- **Effort**: 3 days
- **Acceptance**: Cross-references show semantic relevance labels

### BL-009: Evidence Chain Visual Timeline
- **Purpose**: Improve evidence chain visualization
- **Scope**: Vertical timeline with connectors, step markers, expandable evidence text
- **Dependencies**: BL-004
- **Priority**: Medium
- **Effort**: 3 days
- **Acceptance**: Evidence tab shows vertical timeline with step markers

### BL-010: Node Version History UI
- **Purpose**: Show node version timeline
- **Scope**: Add version history panel to node detail; fetch from KnowledgeStore
- **Dependencies**: BL-003
- **Priority**: Low
- **Effort**: 2 days
- **Acceptance**: Node detail shows version history with timestamps

### BL-011: Graph Visualization View
- **Purpose**: Interactive graph view alongside list view
- **Scope**: Force-directed graph using D3/Cytoscape; click to select node
- **Dependencies**: BL-006
- **Priority**: Low
- **Effort**: 5 days
- **Acceptance**: Graph view tab shows interactive knowledge graph

### BL-012: AI Citation Enhancement
- **Purpose**: Rich citations with evidence levels
- **Scope**: Update `generateCitation()` to include evidence level, confidence, source
- **Dependencies**: BL-003
- **Priority**: Low
- **Effort**: 1 day
- **Acceptance**: Citations show `[L2 Formula: TRN-HA-001 v1.0, L3 Calibration: Own Sign=80]`

---

## SUMMARY

| Priority | Count | Backlogs |
|----------|-------|----------|
| **Critical** | 4 | BL-001, BL-002, BL-003, BL-005 |
| **High** | 2 | BL-004, BL-007 |
| **Medium** | 2 | BL-006, BL-008 |
| **Low** | 3 | BL-009, BL-010, BL-011, BL-012 |

**Total Estimated Effort**: 29 days

**Phase 1 (Critical — 9 days)**: BL-001, BL-002, BL-003, BL-005  
**Phase 2 (High — 4 days)**: BL-004, BL-007  
**Phase 3 (Medium — 5 days)**: BL-006, BL-008  
**Phase 4 (Low — 11 days)**: BL-009, BL-010, BL-011, BL-012

---

**END OF SPECIFICATION**

*This document is the canonical product specification for Knowledge Graph Version 1.0. All implementation must trace to this document.*