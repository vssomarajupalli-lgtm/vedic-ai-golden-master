"""
Vedic AI System — Main Entry Point

Usage:
    python run.py
    python run.py <index_path> <content_path>

Loads machine_index.json + canonical_content.json produced by HoroscopeCleaner_Final,
runs the full deterministic pipeline, and prints structured engine output.
"""
import sys
import os
import json

# Allow running from the backend/ directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.parsers.horoscope_source_loader import HoroscopeSourceLoader
from app.pipeline_runner import PipelineRunner
from app.reports.consultation_summary_generator import ConsultationSummaryGenerator

# ---------------------------------------------------------------------------
# Default file paths (relative to backend/)
# ---------------------------------------------------------------------------
DEFAULT_INDEX_PATH   = os.path.join(os.path.dirname(__file__), "../extracted_json/raju_machine_index.json")
DEFAULT_CONTENT_PATH = os.path.join(os.path.dirname(__file__), "../extracted_json/raju_canonical_content.json")

def main():
    # Accept optional CLI overrides: python run.py <index_path> <content_path>
    index_path   = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INDEX_PATH
    content_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CONTENT_PATH

    print("=" * 64)
    print("  VEDIC AI SYSTEM — Deterministic Astrology Pipeline")
    print("=" * 64)

    # ------------------------------------------------------------------
    # Step 1: Load canonical source files
    # ------------------------------------------------------------------
    print(f"\n[1] Loading source files...")
    print(f"    index   : {os.path.normpath(index_path)}")
    print(f"    content : {os.path.normpath(content_path)}")

    try:
        loader = HoroscopeSourceLoader(index_path, content_path)
        raw_input_data = loader.load()
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  ERROR: {e}")
        sys.exit(1)

    report = raw_input_data.get("_load_report", {})
    print(f"    status  : {report.get('status', 'unknown')}")
    if report.get("warnings"):
        for w in report["warnings"]:
            print(f"    WARNING : {w}")

    # ------------------------------------------------------------------
    # Step 2: Run the pipeline
    # ------------------------------------------------------------------
    print(f"\n[2] Running pipeline...")

    runner = PipelineRunner()
    output = runner.process(raw_input_data)

    # ------------------------------------------------------------------
    # Step 3: Print structured results
    # ------------------------------------------------------------------
    metadata = output.get("metadata", {})
    engines  = output.get("engine_outputs", {})
    master   = output.get("master_probability", {})

    print(f"\n{'=' * 64}")
    print(f"  NATIVE: {metadata.get('name', 'Unknown').upper()}")
    print(f"  LAGNA : {metadata.get('ascendant_sign', '?').capitalize()} "
          f"({metadata.get('ascendant_degree', 0):.1f}°)")
    print(f"{'=' * 64}")

    # --- Master Probability Score ---
    if master:
        m_score  = master.get("final_score", 0)
        m_grade  = master.get("grade", "?")
        m_raw    = master.get("raw_score", 0)
        m_bd     = master.get("breakdown", {})
        m_stubs  = master.get("stub_factors", [])
        bar      = "█" * (m_score // 5) + "░" * (20 - m_score // 5)
        print(f"\n  ┌─ MASTER PROBABILITY SCORE ─────────────────────────────")
        print(f"  │  {m_score:>3}/100  {bar}  {m_grade}")
        print(f"  │  raw={m_raw:.2f}")
        print(f"  ├─ Factor Breakdown ──────────────────────────────────────")
        weights = master.get("weights", {})
        for factor, fscore in m_bd.items():
            w     = weights.get(factor, 0)
            stub  = " [stub]" if factor in m_stubs else ""
            bar_f = "█" * int(fscore // 5) + "░" * (20 - int(fscore // 5))
            print(f"  │  {factor:<20} {fscore:>5.1f}/100  {w*100:>4.0f}%{stub}")
        print(f"  └─────────────────────────────────────────────────────────")

    # --- Natal Promise — Domain Table ---
    natal = engines.get("natal_promise", {})
    if natal:
        DOMAIN_ORDER = [
            "marriage", "career", "wealth", "education",
            "children", "property", "health", "spirituality"
        ]
        print(f"\n  NATAL PROMISE — DOMAIN SCORES")
        print(f"  {'-' * 60}")
        print(f"  {'Domain':<14} {'Score':>5}  {'Bar':<20}  {'Promise':<10}  Karaka")
        print(f"  {'-' * 60}")
        for domain in DOMAIN_ORDER:
            if domain not in natal:
                continue
            d       = natal[domain]
            score   = d.get("score", 0)
            promise = d.get("promise", "?")
            karaka  = d.get("karaka", "?")
            aff     = d.get("afflictions", [])
            bar     = "█" * (score // 5) + "░" * (20 - score // 5)
            aff_s   = f"  ⚠ {', '.join(aff)}" if aff else ""
            print(f"  {domain:<14} {score:>3}/100  {bar}  {promise:<10}  {karaka}{aff_s}")
        print()

    # --- Planet Scores ---
    print(f"\n  PLANET STRENGTH SCORES")
    print(f"  {'-' * 50}")
    planets = engines.get("planets", {})
    for name, data in sorted(planets.items()):
        score       = data.get("final_score", 0)
        base_score  = data.get("base_score")
        bav_modifier = data.get("bav_modifier")
        flags       = data.get("confidence_flags", [])
        flag_s      = f"  [{', '.join(flags)}]" if flags else ""
        bar         = "█" * (score // 5) + "░" * (20 - score // 5)
        if bav_modifier is not None:
            sign  = "+" if bav_modifier >= 0 else ""
            bav_s = f"  [base={base_score} bav={sign}{bav_modifier} → final={score}]"
        else:
            bav_s = ""
        print(f"  {name:<10} {score:>3}/100  {bar}{bav_s}{flag_s}")

    # --- House Scores ---
    print(f"\n  HOUSE STRENGTH SCORES")
    print(f"  {'-' * 50}")
    houses = engines.get("houses", {})
    for house_id in sorted(houses.keys(), key=lambda x: int(x)):
        data   = houses[house_id]
        score  = data.get("final_score", 0)
        flags  = data.get("confidence_flags", [])
        flag_s = f"  [{', '.join(flags)}]" if flags else ""
        bar    = "█" * (score // 5) + "░" * (20 - score // 5)
        print(f"  House {house_id:<4}  {score:>3}/100  {bar}{flag_s}")

    # --- Dasha Activation ---
    print(f"\n  DASHA ACTIVATION (Temporal Layer)")
    print(f"  {'-' * 50}")
    dashas = engines.get("dashas", {})
    if dashas:
        for lord, data in dashas.items():
            if lord == "synthesis" or not isinstance(data, dict):
                continue
            activation = data.get("temporal_activation", {})
            level      = activation.get("active_dasha_level", "?")
            multiplier = activation.get("timing_multiplier", 1.0)
            base_score = data.get("final_score", 0)
            flags      = data.get("confidence_flags", [])
            print(f"  {lord:<10} [{level:<12}]  base={base_score:>3}  "
                  f"multiplier={multiplier:.2f}  flags={flags}")
    else:
        print("  (No active dasha data found in source file)")

    # --- Varga Summary ---
    print(f"\n  VARGA MODIFIERS (D9 / D10)")
    print(f"  {'-' * 50}")
    vargas = engines.get("vargas", {})
    for name, data in sorted(vargas.items()):
        modifiers = data.get("modifiers", {})
        flags     = data.get("confidence_flags", [])
        if modifiers or flags:
            print(f"  {name:<10} modifiers={modifiers}  flags={flags}")

    # --- Rasi Scores ---
    print(f"\n  RASI STRENGTH SCORES (12 Signs)")
    print(f"  {'-' * 50}")
    rasis = engines.get("rasis", {})
    from app.config.astrology_constants import SIGNS_IN_ORDER
    for sign in SIGNS_IN_ORDER:
        if sign not in rasis:
            continue
        data   = rasis[sign]
        score  = data.get("final_score", 0)
        grade  = data.get("grade", "?")
        lord   = data.get("metadata", {}).get("lord", "?")
        flags  = data.get("confidence_flags", [])
        occ    = data.get("metadata", {}).get("occupants", [])
        flag_s = f"  [{', '.join(flags)}]" if flags else ""
        occ_s  = f" occ={occ}" if occ else ""
        bar    = "█" * (score // 5) + "░" * (20 - score // 5)
        print(f"  {sign:<14} {score:>3}/100  {bar}  {grade:<10} lord={lord}{occ_s}{flag_s}")

    # --- Ashtakavarga Engine ---
    print(f"\n  ASHTAKAVARGA — PLANET BAV SUPPORT")
    print(f"  {'-' * 50}")
    av      = engines.get("ashtakavarga", {})
    pb_supp = av.get("planet_bav_support", {})
    from app.config.astrology_constants import BAV_PLANETS
    for planet in BAV_PLANETS:
        if planet not in pb_supp:
            continue
        d   = pb_supp[planet]
        mod = d.get("modifier", 0)
        mod_s = f"+{mod}" if mod > 0 else str(mod)
        bar = "█" * d.get("bindus", 0) + "░" * (8 - d.get("bindus", 0))
        print(f"  {planet:<10} H{d.get('house',0):<2}  [{bar}]  "
              f"{d.get('bindus', 0)}/8  {d.get('grade','?'):<10}  modifier={mod_s}")

    # Dasha BAV support
    db     = av.get("dasha_bav_support", {})
    md_d   = db.get("mahadasha",  {})
    ad_d   = db.get("antardasha", {})
    comb   = db.get("combined_dasha_bav_score", 0)
    conf   = db.get("timing_confidence", "?")
    mult   = db.get("timing_confidence_multiplier", 1.0)
    print(f"\n  ASHTAKAVARGA — DASHA BAV SUPPORT")
    print(f"  {'-' * 50}")
    print(f"  MD ({md_d.get('lord','?'):<8}) H{md_d.get('house',0):<2}  "
          f"bindus={md_d.get('bindus','?')}  grade={md_d.get('grade','?'):<10}  "
          f"confidence={md_d.get('timing_confidence','?')}")
    print(f"  AD ({ad_d.get('lord','?'):<8}) H{ad_d.get('house',0):<2}  "
          f"bindus={ad_d.get('bindus','?')}  grade={ad_d.get('grade','?'):<10}  "
          f"confidence={ad_d.get('timing_confidence','?')}")
    print(f"  Combined BAV score: {comb:.1f}  →  {conf.upper()} confidence  "
          f"(×{mult:.2f} timing multiplier)")

    # SAV analytics summary
    sa = av.get("sav_analytics", {})
    print(f"\n  ASHTAKAVARGA — SAV ANALYTICS")
    print(f"  {'-' * 50}")
    print(f"  Total bindus      : {sa.get('total_bindus', '?')}  "
          f"(avg {sa.get('average_per_house', '?')}/house)")
    print(f"  Peak house        : H{sa.get('peak_house', '?')}  |  "
          f"Weakest house : H{sa.get('weakest_house', '?')}")
    print(f"  Favorable (≥28)   : {sa.get('favorable_houses', [])}")
    print(f"  Unfavorable (<22) : {sa.get('unfavorable_houses', [])}")
    consistency = "✓ Consistent" if sa.get("bav_consistency_check") else "⚠ Mismatch detected"
    print(f"  BAV consistency   : {consistency}")

    # --- Question Engine — Sample Q&A ---
    print(f"\n  QUESTION ENGINE — SAMPLE QUERIES")
    print(f"  {'-' * 60}")
    questions  = [
        "Will I get married?",
        "Will my career improve?",
        "Will I have children?",
        "How is my health?",
        "Will I become wealthy?",
    ]
    evaluated_questions = []
    for q in questions:
        ans    = runner.answer_question(q, output)
        ans["question"] = q
        evaluated_questions.append(ans)
        domain = ans["domain"] or "(unknown)"
        prob   = ans["probability"]
        natal  = ans["natal_promise"]
        timing = ans["timing"]
        print(f"  Q: {q}")
        print(f"     Domain   : {domain:<14}  Natal: {natal['score']:>3}/100 ({natal['promise']})")
        print(f"     Prob     : {prob['score']:>3}/100 ({prob['grade']:<10})  "
              f"Dasha: {timing.get('mahadasha','?').capitalize()} MD / "
              f"{timing.get('antardasha','?').capitalize()} AD  "
              f"[{timing.get('activation_level','?')}]")
        if natal.get("afflictions"):
            print(f"     ⚠ Afflictions: {', '.join(natal['afflictions'])}")
        print()

    if "engine_outputs" not in output:
        output["engine_outputs"] = {}
    output["engine_outputs"]["question_engine"] = evaluated_questions

    # Generate Consultation Summary (Version 1.1 Enhancement)
    try:
        print("\n[3] Generating Consultation Summary (APSE)...")
        csg = ConsultationSummaryGenerator()
        summary_path = os.path.join(os.path.dirname(__file__), "../outputs/consultation_summary.html")
        csg.generate_html(output, output_path=summary_path)
        print(f"    -> Saved to: {os.path.normpath(summary_path)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"    -> Error generating Consultation Summary: {e}")

    print(f"{'=' * 64}")
    print(f"  Pipeline complete. All engines executed deterministically.")
    print(f"{'=' * 64}\n")

if __name__ == "__main__":
    main()
