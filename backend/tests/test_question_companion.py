"""P1 Question Engine companion tests.

Covers the additive ``report_type=question-companion`` JSON data layer:
  - 83-question catalogue / 11 domains / unique IDs
  - 65 evaluated + 18 NOT EVALUATED split (domain coverage rule)
  - NOT EVALUATED entries contain NO score/grade/probability/timing fields
  - client identity reuses the single authoritative main-report chain
  - default main-report endpoint behaviour is unchanged
  - EN / TE real-data runs (skipped when MVS Prasad sources are unavailable)

The registry-split/structure tests are hermetic (no engine needed); only the
companion build inside the TestClient tests relies on the real candidate
payloads because it routes through the real PipelineRunner.
"""

import json
import os
import unittest
from unittest import mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.reports.companion_builder import (
    _load_catalog,
    SUPPORTED_DOMAIN_IDS,
    NOT_EVALUATED_STATUS,
    NOT_EVALUATED_REASON,
)
from app.api.v1.endpoints.reports import router

MVS_DIR = r"D:\HoroscopeCleaner_Final\output"

FORBIDDEN_UN_EVALUATED_FIELDS = (
    "score", "grade", "probability", "final_score", "strength",
    "timing", "dasha", "prediction",
)

# Minimal but valid pipeline output for the endpoint test (mirrors
# test_report_builder's mock payload so ReportBuilder stays green).
STUB_PIPELINE_OUTPUT = {
    "metadata": {
        "request_id": "companion-req-1",
        "timestamp_utc": "2026-08-06T00:00:00Z",
        "name": "Test User",
        "dob": "14.05.1980",
        "tob": "12:00",
        "pob": "Mumbai",
        "latitude": 19.076,
        "longitude": 72.8777,
        "timezone": "+05:30",
        "consultation_date": "2026-08-06",
        "ascendant_sign": "Mesha",
    },
    "master_probability": {"final_score": 85.5, "grade": "EXCELLENT"},
    "engine_outputs": {
        "natal_promise": {
            "wealth": {"score": 90, "promise": "HIGH"},
            "career": {"score": 50, "promise": "MODERATE"},
        },
        "dashas": {"synthesis": {"active_md": "Venus", "active_ad": "Jupiter", "active_pd": "Rahu"}},
        "yogas": {"active_yogas": [{"yoga_name": "Ruchaka Yoga", "strength": 80.0}]},
    },
}


def _fake_structured_result(question_id: str) -> dict:
    """Minimal StructuredQuestionResult-shaped dict for hermetic tests."""
    return {
        "question_title": f"Question {question_id}",
        "domain": "Marriage",
        "executive_summary": {"promise_display": "50% (Moderate)"},
    }


class TestRegistryContract(unittest.TestCase):
    """Hermetic: catalogue shape, uniqueness, and the 65/18 support split."""

    def setUp(self):
        self.catalog = _load_catalog()

    def test_catalog_has_83_questions(self):
        self.assertEqual(len(self.catalog), 83)

    def test_question_ids_unique(self):
        ids = [q["question_id"] for q in self.catalog]
        self.assertEqual(len(ids), len(set(ids)))

    def test_catalog_has_11_domains(self):
        domains = {q["domain_name"] for q in self.catalog}
        self.assertEqual(len(domains), 11)

    def test_supported_split_65_and_18(self):
        supported = [q for q in self.catalog if q["domain_id"] in SUPPORTED_DOMAIN_IDS]
        un_evaluated = [q for q in self.catalog if q["domain_id"] not in SUPPORTED_DOMAIN_IDS]
        self.assertEqual(len(supported), 65)
        self.assertEqual(len(un_evaluated), 18)

    def test_unsupported_domains_are_litigation_travel_compatibility(self):
        un_evaluated_domains = {
            q["domain_name"]
            for q in self.catalog
            if q["domain_id"] not in SUPPORTED_DOMAIN_IDS
        }
        self.assertEqual(
            un_evaluated_domains,
            {"Litigation", "Travel", "Compatibility"},
        )


class TestCompanionShape(unittest.TestCase):
    """Companion payload shape with a stub pipeline + stubbed evaluation."""

    def _build(self, question_service_returns=None):
        from app.reports.companion_builder import companion_builder

        fake_results = [
            _fake_structured_result(f"7.{i}")
            for i in range(1, 9)
        ] + [
            _fake_structured_result(f"10.{i}")
            for i in range(1, 9)
        ]
        # 65 supported question results.
        while len(fake_results) < 65:
            fake_results.append(_fake_structured_result(f"q-{len(fake_results)}"))
        fake_results = fake_results[:65]

        evaluated_qs = [
            q["question_id"]
            for q in _load_catalog()
            if q["domain_id"] in SUPPORTED_DOMAIN_IDS
        ]
        with mock.patch(
            "app.reports.companion_builder.question_service.evaluate_many",
            return_value=(fake_results, []),
        ) as m:
            payload = companion_builder.build(STUB_PIPELINE_OUTPUT, {"native_info": {"name": "Test User"}})
            self.assertEqual(m.call_count, 1)
            self.assertEqual(m.call_args[1]["question_ids"], evaluated_qs)
        return payload

    def test_top_level_keys(self):
        payload = self._build()
        self.assertEqual(
            set(payload.keys()),
            {"report_type", "client_profile", "metadata", "question_catalog",
             "question_results", "question_un_evaluated"},
        )
        self.assertEqual(payload["report_type"], "question-companion")

    def test_client_identity_reuses_authoritative_chain(self):
        payload = self._build()
        # Same single source as the main report: pipeline_meta -> client_profile.
        self.assertEqual(payload["client_profile"]["name"], "Test User")
        self.assertEqual(payload["metadata"]["report_id"], "companion-req-1")

    def test_catalog_results_un_evaluated_counts(self):
        payload = self._build()
        self.assertEqual(len(payload["question_catalog"]), 83)
        self.assertEqual(len(payload["question_results"]), 65)
        self.assertEqual(len(payload["question_un_evaluated"]), 18)

    def test_un_evaluated_entries_have_no_fabricated_fields(self):
        payload = self._build()
        for entry in payload["question_un_evaluated"]:
            self.assertEqual(
                set(entry.keys()),
                {"question_id", "domain", "status", "reason"},
            )
            self.assertEqual(entry["status"], NOT_EVALUATED_STATUS)
            self.assertEqual(entry["reason"], NOT_EVALUATED_REASON)
            for forbidden in FORBIDDEN_UN_EVALUATED_FIELDS:
                self.assertNotIn(forbidden, entry)

    def test_un_evaluated_exact_ids(self):
        payload = self._build()
        catalog = _load_catalog()
        un = {e["question_id"] for e in payload["question_un_evaluated"]}
        unsupported = {
            q["question_id"]
            for q in catalog
            if q["domain_id"] not in SUPPORTED_DOMAIN_IDS
        }
        self.assertEqual(un, unsupported)

    def test_results_ids_match_supported_catalog(self):
        payload = self._build()
        result_titles = [r["question_title"] for r in payload["question_results"]]
        self.assertEqual(len(result_titles), 65)


class TestCompanionDeterminism(unittest.TestCase):
    def test_two_runs_identical(self):
        from app.reports.companion_builder import companion_builder

        fake_results = [_fake_structured_result(f"q-{i}") for i in range(65)]
        with mock.patch(
            "app.reports.companion_builder.question_service.evaluate_many",
            return_value=(fake_results, []),
        ):
            a = companion_builder.build(STUB_PIPELINE_OUTPUT, None)
            b = companion_builder.build(STUB_PIPELINE_OUTPUT, None)
        # client_profile.generated_at is the existing ReportBuilder wall-clock
        # field (unchanged authoritative chain); normalize it for comparison.
        a.setdefault("client_profile", {}).pop("generated_at", None)
        b.setdefault("client_profile", {}).pop("generated_at", None)
        self.assertEqual(a, b)


class TestGenerateReportEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = FastAPI()
        app.include_router(router)
        cls.client = TestClient(app)

    @staticmethod
    def _payload():
        return {
            "canonical_content": {"metadata": {"name": "Test User"}},
            "machine_index": {"native_info": {"name": "Test User"}},
        }

    def test_report_type_question_companion_returns_companion(self):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline

        fake_results = [_fake_structured_result(f"q-{i}") for i in range(65)]
        with mock.patch.object(reports_pipeline, "process", return_value=STUB_PIPELINE_OUTPUT), \
             mock.patch("app.reports.companion_builder.question_service.evaluate_many",
                        return_value=(fake_results, [])):
            resp = self.client.post(
                "/generate-report",
                params={"report_type": "question-companion"},
                json=self._payload(),
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["report_type"], "question-companion")
        self.assertEqual(len(data["question_catalog"]), 83)
        self.assertEqual(len(data["question_results"]), 65)
        self.assertEqual(len(data["question_un_evaluated"]), 18)

    def test_report_type_question_companion_html_is_501(self):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline

        fake_results = [_fake_structured_result(f"q-{i}") for i in range(65)]
        with mock.patch.object(reports_pipeline, "process", return_value=STUB_PIPELINE_OUTPUT), \
             mock.patch("app.reports.companion_builder.question_service.evaluate_many",
                        return_value=(fake_results, [])):
            resp = self.client.post(
                "/generate-report",
                params={"format": "html", "report_type": "question-companion"},
                json=self._payload(),
            )
        self.assertEqual(resp.status_code, 501)

    def test_default_report_type_main_unchanged(self):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline
        from app.services.question_service import question_service

        with mock.patch.object(reports_pipeline, "process", return_value=STUB_PIPELINE_OUTPUT), \
             mock.patch.object(question_service, "answer_structured_question",
                               return_value=_fake_structured_result("7.1")):
            resp = self.client.post(
                "/generate-report",
                json=self._payload(),
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # Default main report path: no companion keys, main sections present.
        self.assertNotIn("report_type", data)
        self.assertNotIn("question_catalog", data)
        self.assertNotIn("question_un_evaluated", data)
        self.assertIn("question_responses", data)
        self.assertIn("client_profile", data)
        self.assertIn("metadata", data)


@unittest.skipUnless(os.path.isdir(MVS_DIR), "MVS Prasad output sources not available")
class TestMvsPrasadRealData(unittest.TestCase):
    """Real MVS Prasad EN + TE runs through the actual PipelineRunner."""

    @classmethod
    def setUpClass(cls):
        from app.pipeline_runner import PipelineRunner
        from app.reports.companion_builder import companion_builder

        cls.runner = PipelineRunner()
        cls.companion_builder = companion_builder
        cls.payloads = {}
        for lang in ("en", "te"):
            canonical_path = os.path.join(MVS_DIR, f"mvs prasad {lang}_canonical_content.json")
            index_path = os.path.join(MVS_DIR, f"mvs prasad {lang}_machine_index.json")
            if not (os.path.isfile(canonical_path) and os.path.isfile(index_path)):
                raise unittest.SkipTest(f"MVS Prasad {lang} sources missing")
            cls.payloads[lang] = (
                json.load(open(canonical_path, encoding="utf-8-sig")),
                json.load(open(index_path, encoding="utf-8-sig")),
            )

    def _build(self, lang):
        canon, mi = self.payloads[lang]
        raw = dict(canon)
        raw["_machine_index"] = mi
        outputs = self.runner.process(raw)
        return self.companion_builder.build(outputs, mi)

    def test_en_counts(self):
        payload = self._build("en")
        self.assertEqual(payload["report_type"], "question-companion")
        self.assertEqual(len(payload["question_catalog"]), 83)
        self.assertEqual(len(payload["question_results"]), 65)
        self.assertEqual(len(payload["question_un_evaluated"]), 18)
        self.assertEqual(payload["client_profile"]["name"], "mvs prasad")

    def test_te_counts(self):
        payload = self._build("te")
        self.assertEqual(len(payload["question_catalog"]), 83)
        self.assertEqual(len(payload["question_results"]), 65)
        self.assertEqual(len(payload["question_un_evaluated"]), 18)
        self.assertEqual(payload["client_profile"]["name"], "mvs prasad")

    def test_en_un_evaluated_has_no_fabricated_fields(self):
        payload = self._build("en")
        for entry in payload["question_un_evaluated"]:
            self.assertEqual(entry["status"], NOT_EVALUATED_STATUS)
            self.assertEqual(
                set(entry.keys()),
                {"question_id", "domain", "status", "reason"},
            )
            for forbidden in FORBIDDEN_UN_EVALUATED_FIELDS:
                self.assertNotIn(forbidden, entry)

    def test_en_te_identical_ids(self):
        en = self._build("en")
        te = self._build("te")
        en_ids = {r["question_title"] for r in en["question_results"]}
        te_ids = {r["question_title"] for r in te["question_results"]}
        self.assertEqual(en_ids, te_ids)

    def test_deterministic_given_same_pipeline_output(self):
        # The pipeline emits a fresh wall-clock timestamp_utc per process();
        # given the SAME engine output, the companion payload must be stable
        # after normalizing that runtime field.
        canon, mi = self.payloads["en"]
        raw = dict(canon)
        raw["_machine_index"] = mi
        outputs = self.runner.process(raw)
        a = self.companion_builder.build(outputs, mi)
        b = self.companion_builder.build(outputs, mi)
        a["metadata"].pop("generated_at", None)
        b["metadata"].pop("generated_at", None)
        a["client_profile"].pop("generated_at", None)
        b["client_profile"].pop("generated_at", None)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()