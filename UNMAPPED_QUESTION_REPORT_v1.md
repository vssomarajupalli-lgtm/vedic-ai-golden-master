# UNMAPPED QUESTION REPORT v1

## 1. Overview
This report identifies the gaps in Formula coverage relative to the target Canonical Question Registry (~500 Questions). It highlights the domains and specific seeds that currently possess 0% formula support.

## 2. Seed Questions Currently Stripped/Unmapped
During the Phase 14E.1 Pilot Implementation, several seed questions were temporarily unmapped because their domains were excluded from the pilot scope, or they require unique mathematical rules not yet implemented.

| Question ID | Question Name       | Target Domain | Reason for Gap |
|-------------|---------------------|---------------|----------------|
| 7.8         | Divorce Risk        | Marriage      | Requires `MAR_RISK_BASE` implementation. |
| 10.6        | Foreign Career      | Career        | Requires 12th house logic variant. |

## 3. Domains with 0% Formula Coverage
The following astrological domains currently possess zero Formula Families, zero Variants, and zero mapped Question IDs. Any API request targeting these domains will return an immediate `missing_registry_entry` error from the Question Router.

- **Domain 4:** Property & Vehicles
- **Domain 5/9:** Education
- **Domain 5:** Children & Progeny
- **Domain 6:** Health & Vitality
- **Domain 6/12:** Enemies & Litigation
- **Domain 7/11:** Business Partnerships & Relationships
- **Domain 9/12:** Travel & Relocation
- **Domain 9/12:** Spirituality & Occult

## 4. Assessment of Remaining Work
Based on the Phase 14C projections, ~493 specific natural language questions remain unsupported. To support them, the system must implement the remaining ~32 Base Families and ~94 Variants documented in the Formula Family Catalog.
