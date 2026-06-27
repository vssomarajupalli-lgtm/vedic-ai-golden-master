# PHASE 14G: ASTROLOGICAL HARDENING REVIEW

## CHILDREN (Progeny)

**1. Why is Moon absent?**
* **Rationale:** The Moon rules the mind and emotions. While it plays a role in female fertility, the primary Parashari indicators for the creation of offspring are the 5th house and Jupiter. Adding the Moon dilutes the physical promise of a child with emotional desire for a child.
* **Classification:** **Intentionally Excluded** (For baseline promise).

**2. Does the engine expose Putrakaraka?**
* **Rationale:** The schema explicitly requests `jupiter`, which is the Naisargika (Natural) Putrakaraka in Parashari astrology. However, if you are referring to the Jaimini *Chara Putrakaraka* (PK - the planet with the 5th highest degree), the current `NatalPromiseEngine` does not extract Chara Karakas. 
* **Classification:** **Future Enhancement** (Jaimini PK extraction).

**3. Why is D7 (Saptamsha) not requested?**
* **Rationale:** The schema must remain decoupled from specific Vargas. It asks for `5th_house_strength`. Currently, the `NatalPromiseEngine` evaluates the D1 5th house. When the Varga expansion occurs (Phase 16+), the engine will automatically blend the D7 Lagna/5th house into that single `5th_house_strength` boolean. Requesting D7 explicitly at the formula level breaks engine abstraction.
* **Classification:** **Future Enhancement** (Upgraded invisibly downstream).

---

## LITIGATION (Conflict & Debts)

**4. Why is 8th House excluded?**
* **Rationale:** The 6th house governs manageable debts, active enemies, and civil lawsuits (competition). The 8th house governs catastrophic ruin, bankruptcy, criminal sentencing, and imprisonment. Merging them confuses a civil lawsuit with a criminal conviction.
* **Classification:** **Intentionally Excluded** (Belongs in a future `LIT_RUIN_RISK` or `WEA_BANKRUPTCY` formula).

**5. Why is Rahu excluded?**
* **Rationale:** Rahu governs deception, fraud, false accusations, and foreign legal battles. It is the primary trigger for sudden, unexpected legal attacks. It was an oversight to exclude it.
* **Classification:** **Recommended Now** (Should be added to `LIT_CONFLICT_BASE`).

---

## TRAVEL & RELOCATION

**6. Are 4th Lord and 12th Lord already included inside house-strength evaluation?**
* **Rationale:** Yes. When the schema evaluates `12th_house_strength` and `4th_house_afflicted`, the `NatalPromiseEngine` aggregates the house placement, the lord's dignity, and aspects. Explicitly asking for the lords creates redundant arrays.
* **Classification:** **Intentionally Excluded** (Handled natively by the engine).

**7. Why is Saturn absent for permanent settlement?**
* **Rationale:** Saturn is the karaka of exile, duration, and the masses. To leave one's homeland *permanently* (Foreign Settlement), Saturn must heavily influence the 12th house or afflict the 4th house. Rahu represents the foreign culture, but Saturn represents the permanence of leaving home.
* **Classification:** **Mandatory Now** (Must be added to `TRV_RELOCATION_BASE`).

---

## SPIRITUALITY & REMEDIES

**8. Why is Moon excluded?**
* **Rationale:** Spirituality (Moksha) requires Ketu (detachment) and Jupiter (wisdom). However, the Moon is the *Manas* (mind). A severely afflicted Moon cannot meditate or focus on mantras, regardless of Jupiter's strength. Evaluating spiritual inclination without the mind is incomplete.
* **Classification:** **Mandatory Now** (Must be added to `SPR_MOKSHA_BASE`).

**9. Should a future SPR_OCCULT_PATH family exist?**
* **Rationale:** Yes. The current base focuses on Moksha (12th), Dharma (9th), and Ishta Devata (5th). The occult (Astrology, Tantra, hidden knowledge) is governed exclusively by the 8th house and Rahu, which are opposing forces to traditional 9th house Dharma.
* **Classification:** **Future Enhancement** (Create `SPR_OCCULT_BASE`).

---

## RELATIONSHIPS & COMPATIBILITY

**10. Why is Mars excluded?**
* **Rationale:** Mars causes *Kuja Dosha* (Manglik). It represents anger, sudden breaks, and violence. It is the primary malefic trigger for divorce and marital destruction in Parashari astrology. It must be evaluated for divorce risk.
* **Classification:** **Mandatory Now** (Must be added to `REL_DYNAMICS_BASE`).

**11. Why is Jupiter excluded?**
* **Rationale:** In female charts, Jupiter is the *Pati Karaka* (Significator of the Husband) in traditional Parashari astrology, just as Venus is the *Kalatra Karaka* (Wife) for men. Excluding Jupiter means female charts are systematically under-evaluated for marital harmony.
* **Classification:** **Mandatory Now** (Must be added to `REL_DYNAMICS_BASE`).

**12. Confirm how D9 influences relationship evaluation.**
* **Rationale:** Exactly like D7 for children. The schema requests `7th_house_strength`. The `NatalPromiseEngine` automatically evaluates the D1 7th house, then silently evaluates the Navamsha (D9) Lagna and 7th house, blending them into a final boolean output. The schema JSON remains clean and Varga-agnostic.
* **Classification:** **Intentionally Excluded** (Handled natively by downstream D9 engine integration).
