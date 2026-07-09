# FORMULA IMPACT MATRIX

The following table demonstrates the structural changes to the Formula Registry before and after the Mandali Decoupling Refactor.

| Formula Key | Current Required Engines | New Required Engines | Current Required Layers | New Required Layers |
| :--- | :--- | :--- | :--- | :--- |
| `MAR_TIMING_BASE` | Promise, Dasha, Transit | Promise, Dasha | `jupiter_transit...` (3 total) | 2 Dasha layers only |
| `CAR_CHANGE_TIMING` | Transit | None (Inherits Base) | `transit_saturn...` (2 total) | 1 Dasha layer only |
| `HLT_LONGEVITY_BASE` | Promise, Dasha, Transit | Promise, Dasha | None | None |
| `HLT_VITALITY_BASE` | Promise, Dasha, Transit | Promise, Dasha | None | None |
| `HLT_RECOVERY_TIMING` | Inherits Base | Inherits Base | `transit_jupiter...` (2 total) | 1 Dasha layer only |
| `AST_PROPERTY_BASE` | Promise, Dasha, Transit | Promise, Dasha | None | None |
| `AST_PROP_TIMING` | Inherits Base | Inherits Base | `transit_jupiter...` (3 total) | 2 Dasha layers only |
| `FAM_PROGENY_BASE` | Promise, Dasha, Transit | Promise, Dasha | None | None |
| `FAM_CHILD_TIMING` | Inherits Base | Inherits Base | `transit_jupiter...` (2 total) | 1 Dasha layer only |

*Note: All instances of `future_gochara_required = True` are permanently deleted across all schemas.*
