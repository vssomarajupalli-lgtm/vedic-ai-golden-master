"""
Vedic AI Golden Master — Batch Report Driver (add-only, thin).

Replicates exactly the production report path implemented by the
`POST /api/v1/reports/generate-report` endpoint (app/api/v1/endpoints/reports.py)
so that every valid `<name>_canonical_content.json` + `<name>_machine_index.json`
pair found in the configured HoroscopeCleaner output folder produces:

    outputs\\batch\\<name>_report.html
    outputs\\batch\\<name>_report.pdf

No engine, formula, schema, registry, or PipelineRunner code is modified.
This driver only discovers pairs and calls the existing production classes.

Usage:
    python batch_reports.py [input_dir] [output_dir]

    input_dir  : HoroscopeCleaner output folder (default D:\\HoroscopeCleaner_Final\\output)
    output_dir : where reports are written   (default <repo>/outputs/batch)
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


def main():
    input_dir  = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_DIR
    output_dir = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR

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
    from app.services.question_service import question_service

    runner          = PipelineRunner()
    report_builder  = ReportBuilder()
    html_generator  = HTMLGenerator()
    pdf_generator   = PDFGenerator()

    html_ok = 0
    pdf_ok  = 0
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

            # 6. PDF report (PDFGenerator handles WeasyPrint -> Playwright fallback).
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