# QUESTION REGISTRY MAPPING v1

## Data Model Specification
Each question in the registry must conform to the following properties:

- `question_id`: Unique identifier (e.g., `MAR_TIMING_001`).
- `question_text`: Default natural language representation.
- `domain`: High-level domain matching the engines (e.g., `marriage`, `career`).
- `subdomain`: Granular focus area (e.g., `timing`, `growth`, `foreign`).
- `house_focus`: Primary houses to evaluate (array of integers).
- `planet_focus`: Primary karakas (significators) to evaluate (array of strings).
- `required_engines`: Internal mathematical engines required to answer this.
- `timing_required`: Boolean. If yes, explicitly triggers Dasha evaluations.
- `future_gochara_required`: Boolean. If yes, triggers Mandali Transit Layer.
- `future_ashtakavarga_required`: Boolean. If yes, triggers BAV Timing Confidence.

---

## 7. Marriage Domain (Sample Extracted Mapping)

### 7.1 Marriage Prospects
```yaml
question_id: MAR_PROS_001
question_text: "Will I get married?"
domain: marriage
subdomain: promise
house_focus: [7, 2, 11]
planet_focus: ["venus", "jupiter"]
required_engines: ["natal_promise", "yogas"]
timing_required: false
future_gochara_required: false
future_ashtakavarga_required: false
```

### 7.2 Marriage Timing
```yaml
question_id: MAR_TIMING_001
question_text: "When will I get married?"
domain: marriage
subdomain: timing
house_focus: [7, 2, 11]
planet_focus: ["venus", "jupiter"]
required_engines: ["natal_promise", "dasha", "transit"]
timing_required: true
future_gochara_required: true
future_ashtakavarga_required: true
```

### 7.3 Delay in Marriage
```yaml
question_id: MAR_DELAY_001
question_text: "Why is my marriage delayed?"
domain: marriage
subdomain: delay
house_focus: [7, 8, 12]
planet_focus: ["saturn", "ketu"]
required_engines: ["natal_promise", "dosha", "yogas"]
timing_required: false
future_gochara_required: false
future_ashtakavarga_required: false
```

### 7.8 Divorce Risk
```yaml
question_id: MAR_DIVORCE_001
question_text: "Is there a risk of divorce?"
domain: marriage
subdomain: separation
house_focus: [6, 8, 12, 7]
planet_focus: ["rahu", "mars", "saturn"]
required_engines: ["natal_promise", "dosha", "transit"]
timing_required: true
future_gochara_required: true
future_ashtakavarga_required: false
```

---

## 10. Career Domain (Sample Extracted Mapping)

### 10.1 Career Growth
```yaml
question_id: CAR_GROWTH_001
question_text: "Will I have a successful career?"
domain: career
subdomain: promise
house_focus: [10, 1, 11]
planet_focus: ["sun", "saturn", "mercury"]
required_engines: ["natal_promise", "yogas"]
timing_required: false
future_gochara_required: false
future_ashtakavarga_required: false
```

### 10.2 Job Change
```yaml
question_id: CAR_CHANGE_001
question_text: "When is a good time to change jobs?"
domain: career
subdomain: timing
house_focus: [10, 5, 9]
planet_focus: ["saturn", "moon"]
required_engines: ["natal_promise", "dasha", "transit"]
timing_required: true
future_gochara_required: true
future_ashtakavarga_required: true
```

### 10.6 Foreign Career
```yaml
question_id: CAR_FOREIGN_001
question_text: "Will I work abroad?"
domain: career
subdomain: foreign
house_focus: [9, 10, 12]
planet_focus: ["rahu", "moon"]
required_engines: ["natal_promise", "yogas"]
timing_required: false
future_gochara_required: false
future_ashtakavarga_required: false
```

---

## 2. Wealth / Family Domain (Sample Extracted Mapping)

### 2.1 Savings Potential
```yaml
question_id: WEA_SAVING_001
question_text: "Will I be able to accumulate wealth?"
domain: wealth
subdomain: savings
house_focus: [2, 11]
planet_focus: ["jupiter", "venus"]
required_engines: ["natal_promise", "yogas"]
timing_required: false
future_gochara_required: false
future_ashtakavarga_required: false
```

### 2.7 Sudden Financial Gains
```yaml
question_id: WEA_SUDDEN_001
question_text: "Will I get sudden wealth or lottery?"
domain: wealth
subdomain: sudden_gains
house_focus: [8, 5, 11]
planet_focus: ["rahu", "jupiter"]
required_engines: ["natal_promise", "yogas", "dasha"]
timing_required: true
future_gochara_required: true
future_ashtakavarga_required: false
```

---

## Timing Governance Application Rule
For ANY question node where `timing_required: true`, the routing engine MUST automatically bind the query to:
1. `engine_outputs.natal_promise[domain]`
2. `engine_outputs.dashas.synthesis.active_md`
3. `engine_outputs.dashas.synthesis.active_ad`
4. `engine_outputs.dashas.synthesis.active_pd`

If `future_gochara_required` or `future_ashtakavarga_required` are `true`, their respective engines are dynamically invoked and appended to the prompt payload sent to the Response Builder.
