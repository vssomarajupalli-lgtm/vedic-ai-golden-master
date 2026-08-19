"""Report manifest builder — release-level provenance for generated reports (D1).

Writes ``<stem>_report_manifest.json`` alongside each generated report so any
canonical JSON / machine index / HTML / PDF can later be traced back to the
exact source files and versions used at generation time.

Scope discipline:
- Presentation/metadata ONLY. Never feeds engine, formula, calibration,
  Gochara/Mandali, dasha, or transit calculations.
- The only time-dependent field is ``generated_at``; the manifest is written
  AFTER the HTML and PDF files are fully written, so every SHA-256 hashes the
  final on-disk bytes.
- A failed/missing PDF produces ``"pdf": null`` (never a fabricated hash).
- Knowledge Graph is intentionally server-only and is never referenced here.
"""
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.reports.schemas import FinalReportSchema
from app.utils.file_hasher import sha256_file

HASH_ALGORITHM = "sha256"
MANIFEST_SCHEMA_VERSION = "1.0"
_REPORT_VERSION = FinalReportSchema.model_fields["report_version"].default


def detect_language(stem: str) -> str:
    """Language from the existing stem convention: a trailing ``en``/``te`` token.

    ``mvs prasad en`` -> ``en``, ``mvs prasad te`` -> ``te``,
    ``J.Divyanshi`` -> ``unknown``.
    """
    token = stem.rsplit(" ", 1)[-1].strip().lower()
    return token if token in ("en", "te") else "unknown"


def build_report_manifest(
    stem: str,
    canonical_path: str,
    machine_index_path: str,
    html_path: str,
    pdf_path: Optional[str],
    person_name: str = "Unknown",
    report_version: str = _REPORT_VERSION,
    engine_version: str = "1.0.0",
    calibration_profile: str = "v1.0_default",
    calibration_version: str = "1.0.0",
    generated_at: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the manifest dict from the exact source/output file paths.

    SHA-256 values are computed from the actual final file bytes. ``pdf_path``
    may be ``None`` (PDF generation failed or was skipped); the manifest then
    records ``"pdf": null``.
    """
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "hash_algorithm": HASH_ALGORITHM,
        "horoscope": {
            "horoscope_id": stem,
            "person_name": person_name,
            "language": detect_language(stem),
        },
        "canonical_content": {
            "filename": os.path.basename(canonical_path),
            "sha256": sha256_file(canonical_path),
        },
        "machine_index": {
            "filename": os.path.basename(machine_index_path),
            "sha256": sha256_file(machine_index_path),
        },
        "html": {
            "filename": os.path.basename(html_path),
            "sha256": sha256_file(html_path),
        },
        "pdf": (
            {
                "filename": os.path.basename(pdf_path),
                "sha256": sha256_file(pdf_path),
            }
            if pdf_path
            else None
        ),
        "versions": {
            "report_version": report_version,
            "engine_version": engine_version,
            "calibration_profile": calibration_profile,
            "calibration_version": calibration_version,
        },
        "generated_at": generated_at
        or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def write_report_manifest(manifest: Dict[str, Any], output_dir: str, stem: str) -> str:
    """Write the manifest JSON alongside the report artifacts."""
    manifest_path = os.path.join(output_dir, stem + "_report_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest_path
