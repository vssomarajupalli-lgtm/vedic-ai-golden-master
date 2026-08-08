# Samartha Vedic AI — Golden Master

## Engineering Freeze Constitution

**Version:** v1.0.0

**Baseline:** GM-017.4

**Status:** ACTIVE

---

## Purpose

This constitution protects the **deterministic astrology core** of the Samartha Vedic AI Golden Master.

The modules declared below are the mathematical, computational, and contractual foundation of the system. They are **permanently frozen** unless a verified calculation defect is proven through the engineering rule defined in this document.

Any change to a frozen module without satisfying the engineering rule is a violation of the production baseline and is prohibited.

---

## Declared Frozen Modules

The following modules are permanently frozen:

- **Astrology Engines**
- **Pipeline Runner**
- **Formula Registry**
- **Formula Verification**
- **Swiss Ephemeris**
- **Planet Strength Engine**
- **House Strength Engine**
- **Dasha Engine**
- **Current Gochara**
- **Mandali Engine**
- **Results Calculation Pipeline**
- **Report JSON Contract**
- **Calibration Framework**

---

## Engineering Rule

No modification to a frozen module may occur unless **all** of the following conditions are satisfied:

1. **A reproducible defect exists** — the defect can be consistently reproduced.
2. **Regression tests prove the issue** — a failing test demonstrates the incorrect behavior against the baseline.
3. **Root cause identified** — the underlying cause is understood and documented.
4. **Change approved** — the change is formally approved under the repository governance and recorded.

If any condition is unmet, the module remains frozen and no change is permitted.

---

## Mandatory Verification

Every future modification — to a frozen module or otherwise — must verify that the following remain unchanged/identical against the last production baseline:

- ✓ Results
- ✓ Formula Verification
- ✓ Consultation
- ✓ Current Gochara
- ✓ Questionnaire
- ✓ Knowledge Graph
- ✓ Print Framework

Regression verification must pass before any merge is approved.

---

## Declaration

**"The deterministic astrology core is hereby frozen under GM-017.4."**

The tag `GM-017.4` (commit `5a0e5883f07f2e8fb54e7167fec2a265d9463c18`) is the official recovery point for this freeze. All future engineering proceeds from this baseline, and no frozen module may be altered without satisfying the Engineering Rule above.
