# Real Horoscope Validation Program (RHVP)
## Operational Workflow

### 1. RHVP Purpose
- Execute deterministic Version 1.0 pipeline
- Collect engineering observations
- Preserve Version 1.0 freeze

### 2. Validation Workflow
CASE
    ↓
Reference canonical JSONs
    ↓
Run deterministic pipeline
    ↓
Generate standard outputs
    ↓
Record observations
    ↓
Proceed to next CASE

### 3. Observation Policy
- One case never changes formulas.
- Observations are collected only.
- Repeated observations may be reviewed later.
- Calibration requires explicit Project Owner approval.

### 4. Folder Structure
The RHVP infrastructure currently relies on the following active folder structure:

```
validation_data/
├── CASE-###/
│   ├── CASE_METADATA.md        (References canonical JSONs)
│   ├── deterministic_output.txt (Standard deterministic outputs)
│   └── validation_notes.md
└── OBSERVATION_REGISTER.md      (Lightweight engineering evidence register)
```
