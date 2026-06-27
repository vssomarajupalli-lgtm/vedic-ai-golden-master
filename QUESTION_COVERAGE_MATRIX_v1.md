# QUESTION COVERAGE MATRIX v1

## 1. Overview
This matrix documents the explicit Many-to-One mapping of Question IDs to their supporting Formula Families and Variants, strictly based on the Phase 14E.1 Pilot Implementation.

## 2. Active Resolving Mappings

All mappings listed below have been successfully tested end-to-end and cleanly resolve through the pipeline.

### Domain 7: Marriage Families
| Question ID | Question Name       | Base Family      | Target Variant       | Resolution Status |
|-------------|---------------------|------------------|----------------------|-------------------|
| 7.1         | Marriage Prospects  | `MAR_TIMING_BASE`| `MAR_TIMING_NORMAL`  | ✅ Active          |
| 7.2         | Marriage Timing     | `MAR_TIMING_BASE`| `MAR_TIMING_NORMAL`  | ✅ Active          |
| 7.3         | Delay in Marriage   | `MAR_TIMING_BASE`| `MAR_TIMING_DELAY`   | ✅ Active          |

### Domain 10: Career Families
| Question ID | Question Name       | Base Family      | Target Variant       | Resolution Status |
|-------------|---------------------|------------------|----------------------|-------------------|
| 10.1        | Career Growth       | `CAR_GROWTH_BASE`| `CAR_PROMOTION_TIMING`| ✅ Active          |
| 10.2        | Job Change          | `CAR_GROWTH_BASE`| `CAR_CHANGE_TIMING`  | ✅ Active          |

### Domain 2: Wealth Families
| Question ID | Question Name       | Base Family      | Target Variant       | Resolution Status |
|-------------|---------------------|------------------|----------------------|-------------------|
| 2.1         | Savings Potential   | `WEA_SUDDEN_BASE`| `WEA_SUDDEN_GAIN`    | ✅ Active          |
| 2.7         | Sudden Gains        | `WEA_SUDDEN_BASE`| `WEA_SUDDEN_GAIN`    | ✅ Active          |

## 3. Analysis of Many-to-One Convergence
The pilot effectively demonstrated the Many-to-One mapping strategy:
- Both 7.1 and 7.2 successfully route to `MAR_TIMING_NORMAL`.
- Both 2.1 and 2.7 successfully route to `WEA_SUDDEN_GAIN`.
By decoupling the semantics from the mathematics, we have achieved a highly resilient, compressed logic layer.
