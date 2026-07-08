# PHASE 13E: PRE-IMPLEMENTATION RISK REVIEW

## 1. Overview
Before implementing the Answer Composer, this review systematically catalogs every potential vulnerability where the generative AI layer could inadvertently breach the strict governance boundaries established in Phase 13D.

---

## 2. Generating New Astrological Conclusions
*The risk of the Composer acting as a mathematical engine rather than a formatter.*

### Risk 2.1: Aspect & Conjunction Inference
- **Failure Mode:** The `isolated_signals` payload contains Venus in the 7th house and Jupiter in the 1st house. The LLM, using its pre-trained astrological knowledge, infers an opposition aspect and generates text about "Jupiter's direct aspect on Venus," even though the Formula Evaluator never evaluated an aspect.
- **Mitigation:** The system prompt must explicitly state: *"Do not calculate, infer, or mention any aspects, conjunctions, or planetary relationships unless they are explicitly written in the EVIDENCE block."*
- **Governance Protection:** Answer Composer Rule 2 ("Never calculate astrology").

### Risk 2.2: Dasha Boundary Hallucination
- **Failure Mode:** The payload indicates the current Mahadasha is Jupiter. The LLM tries to be helpful by predicting exactly when the Jupiter dasha ends, hallucinating a date.
- **Mitigation:** The system prompt must forbid date calculation. Timeline data must only be presented if explicitly provided in the payload.
- **Governance Protection:** Answer Composer Rule 3 ("Never calculate dashas").

---

## 3. Overriding FormulaEvaluator Results
*The risk of the Composer's tone invalidating the deterministic logic.*

### Risk 3.1: Toxic Positivity (Tone Mismatch)
- **Failure Mode:** The Evaluator resolves `final_state = UNFAVORABLE`. However, generative AI models are heavily RLHF-tuned to be helpful and positive. The LLM softens the blow so much ("While this is technically unfavorable, you have absolutely nothing to worry about!") that it completely overrides the mathematical severity.
- **Mitigation:** "Tone-Locking." The prompt template mapping (e.g., `challenging_template`) must contain aggressive system instructions forcing the LLM to remain objective, serious, and focused on remedies, forbidding it from overriding the `final_state`.
- **Governance Protection:** Answer Composer Rule 6 ("Never override Formula Evaluator results").

### Risk 3.2: False Remediation
- **Failure Mode:** The Evaluator resolves `MIXED`. The LLM decides to invent a magical astrological remedy (e.g., "Wear a blue sapphire") to fix the mixed state.
- **Mitigation:** The Answer Composer must be restricted from generating unauthorized remedies. If remedies are needed, they must be pulled from a deterministic remedy database via the Formula Repository, not hallucinated by the LLM.
- **Governance Protection:** Answer Composer Rule 5 ("Never create hidden logic").

---

## 4. Introducing Hidden Scoring
*The risk of the Composer assigning arbitrary weight to the evidence.*

### Risk 4.1: Generative Weighting
- **Failure Mode:** The Evaluator passes three isolated signals: 10th House, Saturn, and Mercury. The LLM arbitrarily decides that Saturn is the most important factor and generates a response that heavily weights Saturn while ignoring Mercury, creating an implicit, hidden scoring system.
- **Mitigation:** The system prompt must explicitly instruct the LLM: *"Present all provided evidence objectively. Do not rank, weight, or state that one astrological factor is more important than another."*
- **Governance Protection:** Core Governance ("No hidden scoring systems").

---

## 5. LLM Hallucination (Pure Fiction)
*The risk of the Composer inventing data out of thin air.*

### Risk 5.1: Phantom Planets
- **Failure Mode:** To make a narrative about marriage flow better, the LLM hallucinates the position of Mars, stating "Because Mars is in your 4th house," even though Mars was completely excluded from the `isolated_signals` by the Formula Evaluator.
- **Mitigation:** The prompt must include a strict exclusionary boundary: *"You are mathematically blind. You may ONLY reference the specific planets and houses listed in the EVIDENCE block below. Do not assume any other planets exist in the user's chart."*
- **Governance Protection:** Input Contract Boundary (Answer Composer Architecture Section 2).

### Risk 5.2: Missing Data Hallucination
- **Failure Mode:** A system degradation occurs (e.g., TransitEngine is down). The LLM is instructed to generate a `MIXED` response. Noticing that transit data is missing from the prompt context, the LLM hallucinates what the current transits *probably* are based on the current calendar date.
- **Mitigation:** The Answer Composer architecture explicitly adopts the **Deterministic** alternative (Phase 13D Section 10). The LLM is never told about missing data or asked to explain it. The system warning is appended as a hardcoded UI block *after* generation, physically preventing the LLM from hallucinating around the failure.
- **Governance Protection:** Future Mandali/Missing Data Protocols (Answer Composer Architecture Section 9).

### Risk 5.4: Evidence Expansion
- **Failure Mode:** Composer expands evaluated evidence into new astrological conclusions that were never evaluated.
- **Mitigation:** Composer may explain evidence but may not derive additional astrological outcomes from that evidence.
- **Governance Protection:** Bounded Evidence Rule.
