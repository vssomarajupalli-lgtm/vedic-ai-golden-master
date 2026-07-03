# FORMULA LIBRARY REVIEW PACK

## 1. Formula Inventory
Based on the current implementation in `backend/app/formulas/registry_data.py`, the following formulas are actively registered in the system:

### Marriage & Relationships
- `MAR_TIMING_BASE`, `MAR_TIMING_NORMAL`, `MAR_TIMING_DELAY`
- `REL_DYNAMICS_BASE`, `REL_MARITAL_HARMONY`, `REL_DIVORCE_RISK`

### Career & Profession
- `CAR_GROWTH_BASE`, `CAR_PROMOTION_TIMING`, `CAR_CHANGE_TIMING`

### Wealth & Finance
- `WEA_SUDDEN_BASE`, `WEA_SUDDEN_GAIN`, `WEA_SUDDEN_LOSS`

### Health & Vitality
- `HLT_LONGEVITY_BASE`, `HLT_LONGEVITY_ASSESSMENT`
- `HLT_VITALITY_BASE`, `HLT_GENERAL_VITALITY`, `HLT_ILLNESS_RISK`, `HLT_RECOVERY_TIMING`

### Property & Assets
- `AST_VEHICLE_BASE`
- `AST_PROPERTY_BASE`, `AST_PROP_PROMISE`, `AST_PROP_TIMING`, `AST_PROP_LOSS_RISK`

### Education
- `EDU_ACADEMIC_BASE`, `EDU_ACADEMIC_SUCCESS`, `EDU_HIGHER_ACADEMICS`, `EDU_FOREIGN_STUDY`, `EDU_EXAM_SUCCESS_TIMING`

### Progeny & Children
- `FAM_PROGENY_BASE`, `FAM_CHILD_PROMISE`, `FAM_CHILD_TIMING`

### Litigation & Conflict
- `LIT_CONFLICT_BASE`, `LIT_LEGAL_VICTORY`, `LIT_DEBT_RISK`, `LIT_CONFLICT_TIMING`

### Travel & Relocation
- `TRV_RELOCATION_BASE`, `TRV_SHORT_TRIP`, `TRV_FOREIGN_SETTLEMENT`, `TRV_TIMING`

### Spirituality
- `SPR_MOKSHA_BASE`, `SPR_SPIRITUAL_PROGRESS`, `SPR_MANTRA_SIDDHI`, `SPR_ISOLATION_TIMING`

---

## 2. Formula Ownership Matrix

| Master Category | Formula Prefix | Core Domain | Secondary Domains |
| :--- | :--- | :--- | :--- |
| Marriage | `MAR_` | Domain 7 | - |
| Career | `CAR_` | Domain 10 | - |
| Wealth | `WEA_` | Domain 2 | Domain 11 |
| Health | `HLT_` | Domain 6 | Domain 8, 12 |
| Assets | `AST_` | Domain 4 | - |
| Education | `EDU_` | Domain 4 | Domain 5, 9 |
| Progeny | `FAM_` | Domain 5 | Domain 9 |
| Litigation | `LIT_` | Domain 6 | - |
| Travel | `TRV_` | Domain 3 | Domain 9, 12 |
| Spirituality | `SPR_` | Domain 9 | Domain 12, 5 |
| Compatibility | `REL_` | Domain 7 | - |

---

## 3. Formula Dependency Map

### Engines
- **NatalPromiseEngine**: Required by **ALL** base formulas.
- **DashaEngine**: Required by `MAR`, `CAR`, `WEA`, `HLT`, `AST_PROPERTY`, `EDU`, `FAM`, `LIT`, `TRV`, `SPR`, `REL`.
- **YogaEngine**: Required by `EDU_ACADEMIC_BASE`.
- **AshtakavargaEngine**: Required by `CAR_GROWTH_BASE`.
- **TransitEngine**: Required by `CAR_CHANGE_TIMING`.

### Key Signals Validated
- **Lagna/Lagna Lord**: Health, Litigation
- **2nd House/Lord**: Wealth, Assets, Compatibility
- **3rd House/Lord**: Travel
- **4th House/Lord**: Assets, Education, Travel
- **5th House/Lord**: Career (Change), Education, Progeny, Spirituality
- **6th House/Lord**: Health, Litigation
- **7th House/Lord**: Marriage, Compatibility
- **8th House/Lord**: Wealth, Health
- **9th House/Lord**: Career, Education, Progeny, Travel, Spirituality
- **10th House/Lord**: Career
- **11th House/Lord**: Career, Wealth, Assets, Litigation
- **12th House/Lord**: Health, Education, Travel, Spirituality

---

## 4. Missing Documentation & Divergence

- **Divergent Prefixes**: The code (`registry_data.py`) implements formulas that deviate from `FORMULA_FAMILY_CATALOG_v1.md`. 
  - Code uses `FAM_`, catalog specifies `PRO_` for Progeny.
  - Code uses `SPR_`, catalog specifies `SPI_` for Spirituality.
- **Missing Families in Catalog**: The `LIT_` (Litigation) family exists in code but is completely missing from the `FORMULA_FAMILY_CATALOG_v1.md`.
- **Missing Code Implementation**: Category 2.10 ("General Life Progress") exists in `FORMULA_CATEGORY_CATALOG_v1.md` but has no corresponding `GEN_` formulas in the codebase.
- **Engine Mismatches**: The architectural documents specify `TransitEngine` and `YogaEngine` for many families (e.g., Marriage, Health, Spirituality), but the actual python seed data restricts them to a very narrow set.

---

## 5. Duplicate Documentation

The formula subsystem suffers from severe documentation fragmentation (13+ Markdown files). The following overlaps cause friction:
- `FORMULA_CATEGORY_CATALOG_v1.md` and `FORMULA_FAMILY_CATALOG_v1.md` define the exact same domain mappings but with slight inconsistencies.
- `FORMULA_DOMAIN_MAP_v1.md` overlaps with the two catalogs mentioned above.
- `FORMULA_REPOSITORY_DATA_MODEL_v1.md` contains a "Seed Formula Blueprints" section which hardcodes formula structures. This is now out-of-sync with the actual source of truth (`backend/app/formulas/registry_data.py`).
- Rationale docs (`EDUCATION_FORMULA_ASTROLOGY_RATIONALE.md`, `HEALTH_FORMULA_ASTROLOGY_RATIONALE.md`, `PROPERTY_FORMULA_ASTROLOGY_RATIONALE.md`) are fragmented across the root directory instead of being unified into a domain-knowledge catalog.

---

## 6. Recommendations

1. **Consolidate Architecture**: Merge the 13+ fragmented `FORMULA_*.md` files into a single, comprehensive `FORMULA_LIBRARY_ARCHITECTURE.md`.
2. **Consolidate Astrology Rationale**: Merge the individual domain rationale documents into a single `ASTROLOGY_RATIONALE_CATALOG.md`.
3. **Single Source of Truth for Data**: Remove all hardcoded "Seed Blueprints" from markdown documents. Markdown should describe the schema, while the python code (`registry_data.py`) dictates the actual inventory.
4. **Align Nomenclature**: Standardize prefixes (e.g., decide between `FAM_` vs `PRO_` and apply strictly across codebase and docs).
5. **Implement Missing Categories**: Add the missing Litigation definitions to the consolidated catalog and address the unimplemented "General Life Progress" category.
