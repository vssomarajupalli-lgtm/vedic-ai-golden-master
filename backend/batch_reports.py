"""
Vedic AI Golden Master — Batch Report Driver (add-only, thin).

Replicates exactly the production report path implemented by the
`POST /api/v1/reports/generate-report` endpoint (app/api/v1/endpoints/reports.py)
so that every valid `<name>_canonical_content.json` + `<name>_machine_index.json`
pair found in the configured HoroscopeCleaner output folder produces:

    outputs\\batch\\<name>_report.html
    outputs\\batch\\<name>_report.pdf

    With the opt-in --companion flag, each pair also produces the Question
    Companion HTML and PDF using exactly the production companion path
    (companion_builder.build(outputs, machine_index) followed by
    companion_html_generator.generate(payload, outputs), then
    PDFGenerator.generate_html on that exact HTML) — the SAME pipeline
    output already computed for the main report is reused; nothing is
    recomputed and no astrology/report logic is duplicated here.

No engine, formula, schema, registry, or PipelineRunner code is modified.
This driver only discovers pairs and calls the existing production classes.
Driving without --companion is byte-for-byte unchanged.

Usage:
    python batch_reports.py [input_dir] [output_dir] [--companion]

    input_dir  : HoroscopeCleaner output folder (default D:\\HoroscopeCleaner_Final\\output)
    output_dir : where reports are written   (default <repo>/outputs/batch)
    --companion: also write <name>_companion.html and <name>_companion.pdf
                 for every pair via the production question-companion path
                 (add-only, opt-in)
"""
import sys
import os
import json
import glob

# Allow running from the backend/ directory regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT_INPUT_DIR  = r"D:\HoroscopeCleaner_Final\output"
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "outputs", "batch")
DEFAULT_QUESTION_IDS = ["10.1", "2.1", "7.1"]


def iter_pairs(input_dir: str):
    """
    Yield (name, canonical_path, machine_index_path) for each valid pair.

    A pair is valid only when both files share the identical filename stem,
    e.g.  raju_canonical_content.json  <->  raju_machine_index.json
    Canonical files without a matching machine index are reported as skipped.
    """
    canonical_files = sorted(glob.glob(os.path.join(input_dir, "*_canonical_content.json")))
    pairs = []
    skipped = []
    for canonical_path in canonical_files:
        base = os.path.basename(canonical_path)
        stem = base[: -len("_canonical_content.json")]
        machine_index_path = os.path.join(input_dir, stem + "_machine_index.json")
        if os.path.isfile(machine_index_path):
            pairs.append((stem, canonical_path, machine_index_path))
        else:
            skipped.append((stem, canonical_path))
    return pairs, skipped


def write_companion_pdf(pdf_generator, comp_html, payload, output_dir, name):
    """Render the companion PDF from the exact companion HTML string.

    Uses the same PDF infrastructure as the main report (WeasyPrint ->
    Playwright fallback) via ``PDFGenerator.generate_html`` — the HTML is
    rendered verbatim; no ``<details open>`` forcing is applied. Returns
    ``(pdf_path, pdf_bytes)``.
    """
    comp_pdf_path = os.path.join(output_dir, name + "_companion.pdf")
    comp_client = str((payload.get("client_profile") or {}).get("name") or "Vedic-AI Report")
    comp_pdf = pdf_generator.generate_html(comp_html, client=comp_client)
    with open(comp_pdf_path, "wb") as f:
        f.write(comp_pdf)
    return comp_pdf_path, comp_pdf


def main():
    # Opt-in companion flag: unknown flags preserved for forward-compat.
    companion = "--companion" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    input_dir  = args[0] if len(args) > 0 else DEFAULT_INPUT_DIR
    output_dir = args[1] if len(args) > 1 else DEFAULT_OUTPUT_DIR

    if not os.path.isdir(input_dir):
        print("[ERROR] Input folder not found: %s" % input_dir)
        return 1

    os.makedirs(output_dir, exist_ok=True)

    pairs, skipped = iter_pairs(input_dir)
    total_canonical = len(pairs) + len(skipped)

    print("=" * 72)
    print("  VEDIC AI GOLDEN MASTER — BATCH REPORT LAUNCHER")
    print("=" * 72)
    print("  Input folder  : %s" % input_dir)
    print("  Output folder : %s" % output_dir)
    print("  Canonical files found : %d" % total_canonical)
    print("  Valid pairs           : %d" % len(pairs))
    print("  Skipped (no index)    : %d" % len(skipped))
    print()

    # Import production components lazily so discovery/reporting still works
    # even if an optional PDF dependency is missing.
    from app.pipeline_runner import PipelineRunner
    from app.reports.builder import ReportBuilder
    from app.reports.html_generator import HTMLGenerator
    from app.reports.pdf_generator import PDFGenerator
    from app.reports.south_indian_chart_data import build_south_indian_chart_data
    from app.reports.report_manifest import build_report_manifest, write_report_manifest
    from app.reports.companion_builder import companion_builder
    from app.reports.companion_html_generator import companion_html_generator
    from app.services.question_service import question_service
    from app.calibration.calibration_manager import CalibrationManager

    runner          = PipelineRunner()
    report_builder  = ReportBuilder()
    html_generator  = HTMLGenerator()
    pdf_generator   = PDFGenerator()

    # Authoritative calibration/version identity (existing single source).
    # Used only for manifest provenance; never fed into engine calculations.
    _calibration  = CalibrationManager()
    _cal_meta     = (_calibration.active_profile or {}).get("metadata", {}) or {}
    _cal_profile  = str(_cal_meta.get("profile_id", "v1.0_default"))
    _cal_version  = str(_cal_meta.get("version", "1.0.0"))

    html_ok = 0
    pdf_ok  = 0
    manifest_ok = 0
    companion_ok = 0
    companion_pdf_ok = 0
    failed  = []

    for name, canonical_path, machine_index_path in pairs:
        print("[%s] Processing %s ..." % ("NEXT", name))
        try:
            canonical        = json.load(open(canonical_path, encoding="utf-8-sig"))
            machine_index    = json.load(open(machine_index_path, encoding="utf-8-sig"))
        except Exception as e:
            failed.append((name, "load", "%s: %s" % (type(e).__name__, e)))
            print("  [%s] Failed to load source files: %s: %s" % ("FAIL", type(e).__name__, e))
            continue

        try:
            # 1. Engine — identical to the /generate-report endpoint path.
            raw_data = dict(canonical)
            raw_data["_machine_index"] = machine_index
            outputs = runner.process(raw_data)

            # 2. Structured question answers — same service the API uses.
            q_responses = []
            for q_id in DEFAULT_QUESTION_IDS:
                q_responses.append(
                    question_service.answer_structured_question(
                        question_id=q_id, pipeline_output=outputs
                    )
                )

            # 3. Report assembly — production ReportBuilder.
            report = report_builder.build_json_report(outputs, machine_index, questions=q_responses)

            # 4. South-Indian chart presentation snapshot (pure passthrough).
            sic_data = build_south_indian_chart_data(raw_data, report)
            if sic_data is not None:
                report["south_indian_chart_data"] = sic_data

            # 5. HTML report.
            html_content = html_generator.generate(report)
            html_path = os.path.join(output_dir, name + "_report.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            html_ok += 1
            print("  [HTML] OK  -> %s (%d bytes)" % (os.path.basename(html_path), len(html_content)))

            # 5B. Question Companion HTML (opt-in only) — exact production path,
            # reusing the SAME outputs already produced for the main report.
            if companion:
                payload = companion_builder.build(outputs, machine_index)
                comp_html = companion_html_generator.generate(payload, outputs)
                comp_path = os.path.join(output_dir, name + "_companion.html")
                with open(comp_path, "w", encoding="utf-8") as f:
                    f.write(comp_html)
                companion_ok += 1
                print("  [COMP] OK  -> %s (%d bytes)" % (os.path.basename(comp_path), len(comp_html)))

                # Companion PDF — same PDF infra as the main report, fed the
                # exact companion HTML string above (no <details> forcing).
                try:
                    comp_pdf_path, comp_pdf = write_companion_pdf(
                        pdf_generator, comp_html, payload, output_dir, name
                    )
                    companion_pdf_ok += 1
                    print("  [COMP-PDF] OK  -> %s (%d bytes)" % (os.path.basename(comp_pdf_path), len(comp_pdf)))
                except Exception as e:
                    failed.append((name, "companion_pdf", "%s: %s" % (type(e).__name__, e)))
                    print("  [COMP-PDF] FAIL -> %s: %s" % (type(e).__name__, e))

            # 6. PDF report (PDFGenerator handles WeasyPrint -> Playwright fallback).
            pdf_path = None
            try:
                pdf_bytes = pdf_generator.generate(report)
                pdf_path = os.path.join(output_dir, name + "_report.pdf")
                with open(pdf_path, "wb") as f:
                    f.write(pdf_bytes)
                pdf_ok += 1
                print("  [PDF ] OK  -> %s (%d bytes)" % (os.path.basename(pdf_path), len(pdf_bytes)))
            except Exception as e:
                failed.append((name, "pdf", "%s: %s" % (type(e).__name__, e)))
                print("  [PDF ] FAIL -> %s: %s" % (type(e).__name__, e))

            # 7. Report manifest (D1) — provenance of source + output artifacts.
            # Hashes the exact final on-disk files. A failed/missing PDF yields
            # "pdf": null (no fabricated hash). Metadata only: never feeds
            # engine, formula, calibration, or Gochara/Mandali calculations.
            try:
                manifest = build_report_manifest(
                    stem=name,
                    canonical_path=canonical_path,
                    machine_index_path=machine_index_path,
                    html_path=html_path,
                    pdf_path=pdf_path,
                    person_name=report.get("client_profile", {}).get("name") or "Unknown",
                    engine_version=_cal_version,
                    calibration_profile=_cal_profile,
                    calibration_version=_cal_version,
                )
                manifest_path = write_report_manifest(manifest, output_dir, name)
                manifest_ok += 1
                print("  [MANI] OK  -> %s" % os.path.basename(manifest_path))
            except Exception as e:
                failed.append((name, "manifest", "%s: %s" % (type(e).__name__, e)))
                print("  [MANI] FAIL -> %s: %s" % (type(e).__name__, e))

        except Exception as e:
            failed.append((name, "processing", "%s: %s" % (type(e).__name__, e)))
            print("  [FAIL] %s: %s" % (type(e).__name__, e))

    # ---- Summary ----
    print()
    print("=" * 72)
    print("  BATCH SUMMARY")
    print("=" * 72)
    print("  Total canonical files found : %d" % total_canonical)
    print("  Valid pairs processed       : %d" % len(pairs))
    print("  HTML reports generated      : %d" % html_ok)
    print("  PDF reports generated       : %d" % pdf_ok)
    print("  Manifests generated         : %d" % manifest_ok)
    if companion:
        print("  Companion HTML generated    : %d" % companion_ok)
        print("  Companion PDF generated     : %d" % companion_pdf_ok)
    print("  Failed                     : %d" % len(failed))
    print("  Skipped (no machine index)  : %d" % len(skipped))
    print("  Output directory            : %s" % output_dir)
    if skipped:
        print()
        print("  Skipped files:")
        for stem, path in skipped:
            print("    - %s (missing %s_machine_index.json)" % (os.path.basename(path), stem))
    if failed:
        print()
        print("  Failed pairs:")
        for name, stage, err in failed:
            print("    - %s  [%s]  %s" % (name, stage, err))
    print()
    print("  Done.")

    return 0


if __name__ == "__main__":
    sys.exit(main())