---
archive_title: "Phase 15G.5 – Yoga Intelligence Trace Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15G.5 – Yoga Intelligence Trace Audit

## 1. Complete Yoga Inventory
The Vedic-AI `YogaEngine` currently evaluates 22 yogas mapped from the `YOGA_REGISTRY`. 

### Categorized Inventory
* **Universal Yogas:** Gaja Kesari Yoga, Neecha Bhanga Raja Yoga, Adhi Yoga
* **Pancha Mahapurusha Yogas:** Ruchaka Yoga, Bhadra Yoga, Hamsa Yoga, Malavya Yoga, Sasa Yoga
* **Wealth Yogas:** Dhana Yoga, Lakshmi Yoga, Vasumathi Yoga
* **Career Yogas:** Raja Yoga, Dharma Karma Adhipati Yoga, Amala Yoga
* **Education Yogas:** Saraswati Yoga, Vidya Yoga
* **Marriage Yogas:** Kalatra Yoga, Saubhagya Yoga
* **Children Yogas:** Putra Yoga, Santana Yoga
* **Spiritual Yogas:** Moksha Yoga, Sanyasa Yoga, Parivraja Yoga

### Structure per Yoga
* **Registry Name:** E.g., `"Bhadra Yoga"`
* **Detection Function:** Specific python method (e.g., `_detect_bhadra_yoga(self, chart_data)`)
* **Current Return Type:** Primitive `bool` (`True` or `False`)
* **Current Output Structure:** If `True`, the registry name is appended as a raw string to an array (e.g., `universal_yogas`, `house_7_yogas`). If `False`, it is silently discarded.

---

## 2. Detection Rule Audit
Every yoga evaluates a hardcoded series of planetary rules. Below is a structural mapping of the rules currently being evaluated silently:

### Example: Pancha Mahapurusha Yogas (Ruchaka, Bhadra, Hamsa, Malavya, Sasa)
- **Planet Conditions:** Specific target planet (Mars, Mercury, Jupiter, Venus, Saturn).
- **House Conditions:** Target planet must be placed in a Kendra (1, 4, 7, 10).
- **Dignity Conditions:** Target planet must be in `own_sign`, `exalted`, or `moolatrikona`.

### Example: Lakshmi Yoga
- **House Conditions:** Lord of the 9th house must be placed in a Kendra.
- **Dignity Conditions:** Lord of the 9th house must be in `own_sign` or `exalted`.
- **Dignity Conditions:** Lord of the 1st house (Lagna Lord) must NOT be `debilitated`.

### Example: Gaja Kesari Yoga
- **House Conditions:** Jupiter and Moon must have valid house placements.
- **Aspect/Relative Conditions:** Jupiter must be in a Kendra relative to the Moon's house position.

---

## 3. Rule Visibility Matrix

| Item | Exists? | Description |
| :--- | :--- | :--- |
| **Rule evaluations** | ❌ No | Boolean checks are evaluated invisibly inside Python `if` statements. |
| **Pass/Fail status** | ❌ No | Only global "Passes" are logged. Failures do not exist in the output. |
| **Failure reason** | ❌ No | The code returns `False` immediately upon the first failed condition. |
| **Intermediate calculations**| ❌ No | Dispositors and relative house offsets are discarded. |
| **Trigger conditions** | ❌ No | Passing criteria are not serialized for the frontend. |

---

## 4. Data Flow Audit
1. **Yoga Registry:** Configures metadata (target houses, domains) mapping strings to rules.
2. **Yoga Engine:** Maps the data over detection stubs. Generates `boolean` outputs.
   * **Where Information is Generated:** Inside methods like `_check_mahapurusha`.
   * **Where Information is Discarded:** Inside the same methods. Failed boolean branches (`return False`) obliterate the trace.
3. **PipelineRunner:** Injects the successful string lists into `engine_outputs.yogas`.
   * **Where Information becomes Invisible:** By the time the PipelineRunner runs, negative space (failed yogas) is completely gone.
4. **API:** Returns arrays of strings inside `ChartProcessResponse`.
5. **Frontend:** Displays `Detected Yogas: X`.

---

## 5. Proposed Yoga Trace Design
To support transparency, the YogaEngine must be refactored from `bool` returns to deterministic Trace Objects.

**Proposed Output Schema (`isolated_yoga_traces`):**
```json
{
  "yoga_name": "Bhadra Yoga",
  "status": "FAILED",
  "rules": [
    {
      "rule": "Mercury must be in a Kendra (1, 4, 7, 10)",
      "result": false
    },
    {
      "rule": "Mercury must be in Own Sign or Exalted",
      "result": true
    }
  ],
  "failure_reason": "Mercury is not placed in a Kendra."
}
```

---

## 6. Verification Console Design (UI)
The frontend Verification Console (and the future Intelligence Console) will consume this schema using a collapsible UI.

**Layout:**
```text
[Bhadra Yoga]  --------------------------------------  [ FAILED ] 
  ▼ Expand
  
  Condition Trace:
  [✓] Mercury must be in Own Sign or Exalted
  [✗] Mercury must be in a Kendra (1, 4, 7, 10)
  
  Conclusion:
  Failure Reason: Mercury is not placed in a Kendra.
```
- **One Expandable Card per Yoga**, grouped by domain/category.
- **Status Badges** indicating `PASSED`, `FAILED`, or `PARTIAL`.
- **Checklist format** displaying exactly which sub-rules successfully validated.

---

## 7. Backward Compatibility Audit
The Yoga Trace architecture can be added 100% nondestructively:
1. **Existing Yoga Detection:** The `YogaEngine.evaluate` method will continue returning its current dictionary of string arrays (`house_1_yogas`, `universal_yogas`) to preserve legacy schemas.
2. **Existing API Responses:** A new parallel key, `yoga_traces`, will be appended to the `YogaEngine` dictionary output. Legacy systems iterating over `house_X_yogas` will not be affected.
3. **Question Engine:** Unaffected.

---

## 8. Implementation Readiness
* **Ready Now:** ❌ No.
* **Requires Backend Changes:** ✅ Yes. `app/engines/yoga_engine.py` needs a complete rewrite of its detection stubs to capture condition variables rather than returning primitive booleans.
* **Requires Schema Changes:** ✅ Yes. A new `yoga_traces` dictionary schema must be exposed via `ChartProcessResponse`.
* **Requires Frontend Changes:** ✅ Yes. `VerificationConsole.tsx` must be extended to parse and render the new `yoga_traces` block into the proposed UI checklist cards.
* **Estimated Effort:** Medium-High. Refactoring 22 distinct mathematical conditions requires surgical care to prevent breaking existing detection rates.
