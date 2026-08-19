import hashlib
import json
import os
import tempfile
import unittest

from app.reports.report_manifest import (
    MANIFEST_SCHEMA_VERSION,
    build_report_manifest,
    detect_language,
    write_report_manifest,
)
from app.utils.file_hasher import sha256_file


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class TestReportManifest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = self._tmp.name

    def _write(self, name, data=b"..."):
        path = os.path.join(self.dir, name)
        with open(path, "wb") as f:
            f.write(data)
        return path

    def _manifest_for(self, stem, canonical=None, index=None, html=None, pdf=None, name="Test Person"):
        canonical = canonical or self._write(stem + "_canonical_content.json", b'{"planets": {}}')
        index = index or self._write(stem + "_machine_index.json", b'[{"title": "x"}]')
        html = html or self._write(stem + "_report.html", b"<html>report</html>")
        manifest = build_report_manifest(
            stem=stem,
            canonical_path=canonical,
            machine_index_path=index,
            html_path=html,
            pdf_path=pdf,
            person_name=name,
        )
        return manifest, canonical, index, html

    # Test 1 — manifest is generated (and persisted on disk).
    def test_manifest_is_generated_and_written(self):
        stem = "mvs prasad te"
        manifest, *_ = self._manifest_for(stem)
        path = write_report_manifest(manifest, self.dir, stem)
        self.assertTrue(os.path.isfile(path))
        with open(path, encoding="utf-8") as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk, manifest)
        self.assertEqual(on_disk["schema_version"], MANIFEST_SCHEMA_VERSION)
        self.assertEqual(on_disk["hash_algorithm"], "sha256")

    # Test 2 — horoscope identity.
    def test_horoscope_identity(self):
        manifest, *_ = self._manifest_for("mvs prasad en")
        self.assertEqual(manifest["horoscope"]["horoscope_id"], "mvs prasad en")
        self.assertEqual(manifest["horoscope"]["person_name"], "Test Person")

    # Test 3 — language identification.
    def test_language_detection(self):
        self.assertEqual(detect_language("mvs prasad en"), "en")
        self.assertEqual(detect_language("mvs prasad te"), "te")
        self.assertEqual(detect_language("J.Divyanshi"), "unknown")
        manifest, *_ = self._manifest_for("mvs prasad te")
        self.assertEqual(manifest["horoscope"]["language"], "te")
        manifest, *_ = self._manifest_for("mvs prasad en")
        self.assertEqual(manifest["horoscope"]["language"], "en")

    # Test 4 — canonical filename correct.
    def test_canonical_filename_correct(self):
        manifest, canonical, _, _ = self._manifest_for("mvs prasad te")
        self.assertEqual(manifest["canonical_content"]["filename"], os.path.basename(canonical))

    # Test 5 — canonical SHA-256 equals independent calculation.
    def test_canonical_sha256_matches_independent(self):
        manifest, canonical, _, _ = self._manifest_for("mvs prasad en")
        with open(canonical, "rb") as f:
            expected = _sha256_bytes(f.read())
        self.assertEqual(manifest["canonical_content"]["sha256"], expected)
        self.assertEqual(manifest["canonical_content"]["sha256"], sha256_file(canonical))

    # Test 6 — machine index SHA-256 correct.
    def test_machine_index_sha256_correct(self):
        manifest, _, index, _ = self._manifest_for("mvs prasad en")
        with open(index, "rb") as f:
            expected = _sha256_bytes(f.read())
        self.assertEqual(manifest["machine_index"]["sha256"], expected)

    # Test 7 — HTML SHA-256 correct (hashed after final write).
    def test_html_sha256_correct(self):
        manifest, _, _, html = self._manifest_for("mvs prasad en")
        with open(html, "rb") as f:
            expected = _sha256_bytes(f.read())
        self.assertEqual(manifest["html"]["sha256"], expected)

    # Test 8 — PDF SHA-256 correct when the PDF exists.
    def test_pdf_sha256_correct_when_present(self):
        pdf = self._write("mvs prasad en_report.pdf", b"%PDF-1.4 fake")
        manifest, *_ = self._manifest_for("mvs prasad en", pdf=pdf)
        with open(pdf, "rb") as f:
            expected = _sha256_bytes(f.read())
        self.assertEqual(manifest["pdf"]["sha256"], expected)
        self.assertEqual(manifest["pdf"]["filename"], os.path.basename(pdf))

    # Test 11 — missing/failed PDF produces no fabricated hash.
    def test_pdf_is_none_when_missing(self):
        manifest, *_ = self._manifest_for("mvs prasad en", pdf=None)
        self.assertIsNone(manifest["pdf"])

    # Test 9 — manifest building never mutates any source/output file.
    def test_manifest_does_not_alter_source_files(self):
        canonical = self._write("x_canonical_content.json", b'{"a": 1}')
        index = self._write("x_machine_index.json", b'[{"t": "u"}]')
        html = self._write("x_report.html", b"<html>h</html>")
        pdf = self._write("x_report.pdf", b"%PDF-1.4 fake")
        before = {
            "c": sha256_file(canonical),
            "i": sha256_file(index),
            "h": sha256_file(html),
            "p": sha256_file(pdf),
        }
        build_report_manifest("x", canonical, index, html, pdf, person_name="N")
        after = {
            "c": sha256_file(canonical),
            "i": sha256_file(index),
            "h": sha256_file(html),
            "p": sha256_file(pdf),
        }
        self.assertEqual(before, after)

    # Test 12 — Telugu and English produce independent correct manifests.
    def test_en_te_independent_manifests(self):
        canonical_te = self._write("mvs prasad te_canonical_content.json", b'{"planets": {"moon": {"sign": "Mesha"}}}')
        canonical_en = self._write("mvs prasad en_canonical_content.json", b'{"planets": {"moon": {"sign": "Aries"}}}')
        manifest_te, *_ = self._manifest_for("mvs prasad te", canonical=canonical_te)
        manifest_en, *_ = self._manifest_for("mvs prasad en", canonical=canonical_en)
        self.assertNotEqual(
            manifest_te["canonical_content"]["filename"],
            manifest_en["canonical_content"]["filename"],
        )
        self.assertEqual(manifest_te["horoscope"]["language"], "te")
        self.assertEqual(manifest_en["horoscope"]["language"], "en")
        self.assertNotEqual(
            manifest_te["canonical_content"]["sha256"],
            manifest_en["canonical_content"]["sha256"],
        )

    # Versions + generated_at contract.
    def test_versions_and_generated_at(self):
        manifest, *_ = self._manifest_for("mvs prasad en")
        self.assertEqual(manifest["versions"]["report_version"], "1.2.0")
        self.assertEqual(manifest["versions"]["calibration_profile"], "v1.0_default")
        self.assertIn("generated_at", manifest)
        self.assertRegex(manifest["generated_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


if __name__ == "__main__":
    unittest.main()
