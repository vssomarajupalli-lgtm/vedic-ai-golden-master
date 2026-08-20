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
import tempfile
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

    def test_report_type_question_companion_html_renders(self):
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
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers.get("content-type", ""))
        html = resp.text
        self.assertIn("Question Companion", html)
        self.assertIn("Test User", html)
        self.assertIn("Total Questions", html)
        # 65 evaluated + 18 NOT EVALUATED cards visible.
        self.assertEqual(html.count("INSUFFICIENT ENGINE DOMAIN COVERAGE"), 18)
        self.assertNotIn("q-999", html)

    def test_report_type_question_companion_grouped_by_domain(self):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline

        catalog = _load_catalog()
        supported = [q for q in catalog if q["domain_id"] in SUPPORTED_DOMAIN_IDS]
        unsupported = [q for q in catalog if q["domain_id"] not in SUPPORTED_DOMAIN_IDS]
        # One result per supported question, carrying its real catalog domain so
        # the template grouping matches the live payload shape.
        fake_results = [
            {"question_title": q["question_name"], "domain": q["domain_name"]}
            for q in supported
        ]
        with mock.patch.object(reports_pipeline, "process", return_value=STUB_PIPELINE_OUTPUT), \
             mock.patch("app.reports.companion_builder.question_service.evaluate_many",
                        return_value=(fake_results, [])):
            resp = self.client.post(
                "/generate-report",
                params={"format": "html", "report_type": "question-companion"},
                json=self._payload(),
            )
        html = resp.text
        self.assertEqual(resp.status_code, 200)
        # Every evaluated registry domain shows up as a section heading.
        evaluated_domains = {q["domain_name"] for q in supported}
        for domain in evaluated_domains:
            self.assertIn(">%s<" % domain, html)
        # Unsupported domains are present and explicitly marked NOT EVALUATED.
        for domain in {q["domain_name"] for q in unsupported}:
            self.assertIn(">%s<" % domain, html)
            self.assertIn("NOT EVALUATED", html)
        # A representative evaluated question title is rendered.
        self.assertIn(supported[0]["question_name"], html)

    def test_report_type_question_companion_pdf_is_501(self):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline

        fake_results = [_fake_structured_result(f"q-{i}") for i in range(65)]
        with mock.patch.object(reports_pipeline, "process", return_value=STUB_PIPELINE_OUTPUT), \
             mock.patch("app.reports.companion_builder.question_service.evaluate_many",
                        return_value=(fake_results, [])):
            resp = self.client.post(
                "/generate-report",
                params={"format": "pdf", "report_type": "question-companion"},
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

    def test_main_html_has_no_companion_leak(self):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline
        from app.services.question_service import question_service

        with mock.patch.object(reports_pipeline, "process", return_value=STUB_PIPELINE_OUTPUT), \
             mock.patch.object(question_service, "answer_structured_question",
                               return_value=_fake_structured_result("7.1")):
            resp = self.client.post(
                "/generate-report",
                params={"format": "html"},
                json=self._payload(),
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers.get("content-type", ""))
        html = resp.text
        self.assertNotIn("question_catalog", html)
        self.assertNotIn("question_un_evaluated", html)
        self.assertNotIn("NOT EVALUATED", html)


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

    def test_en_html_renders(self):
        from app.reports.companion_html_generator import companion_html_generator

        payload = self._build("en")
        html = companion_html_generator.generate(payload)
        self.assertIn("mvs prasad", html)
        self.assertIn("Question Companion", html)
        # All 18 unsupported questions render with the honest reason, none with
        # a fabricated score/grade.
        self.assertEqual(html.count("INSUFFICIENT ENGINE DOMAIN COVERAGE"), 18)
        self.assertNotIn("final_score", html)

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


RAJU_CANONICAL = r"D:\vedic-ai-golden-master\extracted_json\raju_canonical_content.json"
RAJU_INDEX = r"D:\vedic-ai-golden-master\extracted_json\raju_machine_index.json"


def _rich_pipeline_output():
    """Pipeline output with existing Dasha + governed Mandali data (no new calcs).

    Timeline reference window: 2020-01-01 -> 2030-01-01; deterministic
    reference date 2026-08-06. Sade Sati (Rising Current / Setting Upcoming),
    Ardha Ashtama (resolver: one Current, one Completed) and Ashtama Shani
    (Upcoming) windows all overlap the reference window.
    """
    return {
        "metadata": {"name": "Test User", "dob": "14.05.1980"},
        "target_date_utc": "2026-08-06T00:00:00+00:00",
        "master_probability": {"lifetime_projection": []},
        "engine_outputs": {
            "dashas": {
                "synthesis": {
                    "active_md": "Mars", "active_ad": "Sun", "active_pd": "Mercury",
                    "target_date": "2026-08-06",
                },
                "timeline": [
                    {"start_date": "2020-01-01", "end_date": "2023-01-01",
                     "mahadasha": "Mars", "antardasha": "Moon", "pratyantardasha": "Rahu",
                     "dasha_activation": 61.0},
                    {"start_date": "2023-01-01", "end_date": "2030-01-01",
                     "mahadasha": "Mars", "antardasha": "Sun", "pratyantardasha": "Mercury",
                     "dasha_activation": 73.0},
                ],
            },
            "mandali_advisory": {
                "sade_sati": {"cycles": [{"sade_sati_windows": [
                    {"phase": "Rising", "rasi": "Aries", "start": "01.05.2025",
                     "end": "09.04.2027", "mandali": 12},
                    {"phase": "Setting", "rasi": "Gemini", "start": "10.04.2027",
                     "end": "09.04.2029", "mandali": 2},
                ]}]},
                "ashtama_shani": {"cycles": [{"ashtama_shani_windows": [
                    {"phase": "Ashtama", "rasi": "Leo", "start": "01.06.2028",
                     "end": "01.06.2030", "mandali": 8},
                ]}]},
            },
            "mandali_gochar_report": {
                "saturn_periods": {
                    "ardha_ashtama": {
                        "current": [
                            {"mechanism": "MANDALI_RESOLVER", "phase": "Ardha Ashtama",
                             "rasi": "Taurus", "mandali_name": "4",
                             "entry": "01.02.2025", "exit": "02.03.2029"},
                            {"mechanism": "MANDALI_RESOLVER", "phase": "Ardha Ashtama",
                             "rasi": "Taurus", "mandali_name": "4",
                             "entry": "01.03.2021", "exit": "01.04.2023"},
                        ],
                        "upcoming": [],
                    },
                },
            },
        },
    }


class TestQuestionCompanionHtmlSections(unittest.TestCase):
    """P2 additions: dynamic navigation, dasha timeline, special transits, formulas."""

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

    @staticmethod
    def _catalog_domain_results():
        """One result per supported question carrying its real catalog domain."""
        catalog = _load_catalog()
        supported = [q for q in catalog if q["domain_id"] in SUPPORTED_DOMAIN_IDS]
        return [
            {"question_title": q["question_name"], "domain": q["domain_name"]}
            for q in supported
        ]

    def _post_html(self, fake_results, pipeline_output):
        from app.api.v1.endpoints.reports import pipeline as reports_pipeline

        with mock.patch.object(reports_pipeline, "process", return_value=pipeline_output), \
             mock.patch("app.reports.companion_builder.question_service.evaluate_many",
                        return_value=(fake_results, [])):
            return self.client.post(
                "/generate-report",
                params={"format": "html", "report_type": "question-companion"},
                json=self._payload(),
            )

    def test_dynamic_left_navigation(self):
        catalog = _load_catalog()
        fake = self._catalog_domain_results()
        resp = self._post_html(fake, _rich_pipeline_output())
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        # All actual domain groups (registry order) have group anchors + nav links.
        groups = []
        for record in catalog:
            if record["domain_name"] not in groups:
                groups.append(record["domain_name"])
        for i, group in enumerate(groups):
            self.assertIn('id="group-%d"' % i, html)
            self.assertIn('href="#group-%d"' % i, html)
        # First supported question gets a clickable nav item with a card anchor.
        self.assertIn('href="#q-0-0"', html)
        self.assertIn('id="q-0-0"', html)
        # Bottom information sections are navigable.
        for anchor in ("#dasha-timeline", "#special-transit", "#formula-methods"):
            self.assertIn('href="%s"' % anchor, html)
        self.assertIn("Also in this report", html)

    def test_dasha_timeline_renders_existing_rows(self):
        fake = self._catalog_domain_results()
        resp = self._post_html(fake, _rich_pipeline_output())
        html = resp.text
        self.assertIn("Planetary Periods / Dasha Timeline", html)
        self.assertIn("Mahadasha", html)
        self.assertIn("Antardasha", html)
        self.assertIn("Pratyantardasha", html)
        self.assertIn(">Mars<", html)
        self.assertIn(">Sun<", html)

    def test_special_transit_not_applicable_when_no_data(self):
        # Empty engine outputs -> every governed cycle is honestly NOT APPLICABLE.
        empty = {
            "metadata": {"name": "Test User", "dob": "14.05.1980"},
            "target_date_utc": "2026-08-06T00:00:00+00:00",
            "engine_outputs": {"dashas": {"synthesis": {}, "timeline": []}},
        }
        fake = self._catalog_domain_results()
        resp = self._post_html(fake, empty)
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertIn("Special Transit / Mandali Periods", html)
        # One NOT APPLICABLE badge per governed cycle (Sade Sati / Ardha
        # Ashtama / Ashtama) — the honest empty-data presentation.
        self.assertEqual(html.count(">NOT APPLICABLE<"), 3)

    def test_special_transit_applicable_with_statuses(self):
        fake = self._catalog_domain_results()
        resp = self._post_html(fake, _rich_pipeline_output())
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertEqual(html.count("APPLICABLE"), 3)
        self.assertNotIn("NOT APPLICABLE", html)
        # Statuses: Sade Sati Rising Current + Ardha current -> 2 Current,
        # Sade Sati Setting + Ashtama -> 2 Upcoming, Ardha completed -> 1 Completed.
        self.assertGreaterEqual(html.count(">Current<"), 2)
        self.assertGreaterEqual(html.count(">Upcoming<"), 2)
        self.assertGreaterEqual(html.count(">Completed<"), 1)
        for period in ("Sade Sati", "Ardha Ashtama Shani", "Ashtama Shani"):
            self.assertIn(period, html)
        # No fabricated dates: only the governed window dates appear verbatim.
        self.assertIn("01.05.2025", html)
        self.assertIn("01.06.2030", html)

    def test_formula_methods_section(self):
        fake = self._catalog_domain_results()
        resp = self._post_html(fake, _rich_pipeline_output())
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertIn("Formula &amp; Calculation Methods", html)
        self.assertIn("Natal Promise", html)
        # Authoritative registry formula reference for Marriage is rendered.
        self.assertIn("MAR_TIMING_NORMAL", html)
        self.assertIn("Formula references by domain", html)


class TestSaturnOverlapIndicators(unittest.TestCase):
    """P2.2: Saturn overlap labels appended to Future Opportunity lines.

    Validates exact overlap semantics against the existing governed Windows in
    ``_rich_pipeline_output``:
      Sade Sati Rising 01.05.2025-09.04.2027 / Setting 10.04.2027-09.04.2029,
      Ashtama Shani 01.06.2028-01.06.2030, Ardha Ashtama 01.02.2025-02.03.2029
      and 01.03.2021-01.04.2023.
    """

    @staticmethod
    def _payload_with_windows(windows):
        catalog = [{
            "question_id": "marriage_1",
            "domain_id": 4,
            "domain_name": "Marriage",
            "question_name": "When will I get married?",
            "formula_key": "MAR_TIMING_NORMAL",
        }]
        result = {
            "question_title": "Marriage Timing",
            "domain": "Marriage",
            "future_opportunities": windows,
        }
        return {
            "report_type": "question-companion",
            "client_profile": {"name": "Test User"},
            "metadata": {},
            "question_catalog": catalog,
            "question_results": [result],
            "question_un_evaluated": [],
        }

    @staticmethod
    def _render(windows, pipeline_output=None):
        from app.reports.companion_html_generator import companion_html_generator
        return companion_html_generator.generate(
            TestSaturnOverlapIndicators._payload_with_windows(windows),
            _rich_pipeline_output() if pipeline_output is None else pipeline_output,
        )

    @staticmethod
    def _pipeline_with_cycle(cycle_key):
        """Rich pipeline restricted to one governed Saturn cycle (+ empty others)."""
        po = _rich_pipeline_output()
        advisory = po["engine_outputs"]["mandali_advisory"]
        po["engine_outputs"]["mandali_advisory"] = {
            "sade_sati": {"cycles": [{"sade_sati_windows": []}]},
            "ashtama_shani": {"cycles": [{"ashtama_shani_windows": []}]},
        }
        po["engine_outputs"]["mandali_advisory"][cycle_key] = advisory[cycle_key]
        po["engine_outputs"]["mandali_gochar_report"] = {
            "saturn_periods": {"ardha_ashtama": {"current": [], "upcoming": []}},
        }
        return po

    @staticmethod
    def _window(start, end):
        return {
            "rank": 1,
            "start_date": start,
            "end_date": end,
            "age": "46",
            "mahadasha": "Mars",
            "antardasha": "Sun",
            "pratyantardasha": "Mercury",
            "final_probability_display": "52% (Good)",
        }

    def test_overlap_appends_single_label(self):
        html = self._render(
            [self._window("15 Jun 2026", "15 Nov 2026")],
            self._pipeline_with_cycle("sade_sati"),
        )
        # Sade Sati Rising window contains the whole Future Opportunity window.
        self.assertIn(
            "MD: Mars &middot; AD: Sun &middot; PD: Mercury &middot; "
            "Period: 15 Jun 2026 &rarr; 15 Nov 2026 &middot; "
            "Probability: 52% (Good) &middot; <strong>Sade Sati</strong>",
            html,
        )
        self.assertNotIn("<strong>Ashtama Shani</strong>", html)
        self.assertNotIn("<strong>Ardha Ashtama Shani</strong>", html)

    def test_overlap_appends_ashtama_label(self):
        html = self._render(
            [self._window("01 Jan 2029", "01 Dec 2029")],
            self._pipeline_with_cycle("ashtama_shani"),
        )
        self.assertIn("&middot; <strong>Ashtama Shani</strong>", html)
        self.assertNotIn("<strong>Sade Sati</strong>", html)

    def test_multiple_overlaps_show_all_labels(self):
        html = self._render([self._window("01 Mar 2025", "01 May 2029")])
        for label in ("<strong>Sade Sati</strong>",
                      "<strong>Ashtama Shani</strong>",
                      "<strong>Ardha Ashtama Shani</strong>"):
            self.assertIn(label, html)

    def test_no_overlap_adds_nothing(self):
        html = self._render([self._window("01 Jan 2020", "01 Dec 2020")])
        self.assertNotIn("<strong>Sade Sati</strong>", html)
        self.assertNotIn("<strong>Ashtama Shani</strong>", html)
        self.assertNotIn("<strong>Ardha Ashtama Shani</strong>", html)
        # The existing line renders unchanged.
        self.assertIn(
            "MD: Mars &middot; AD: Sun &middot; PD: Mercury &middot; "
            "Period: 01 Jan 2020 &rarr; 01 Dec 2020 &middot; Probability: 52% (Good)",
            html,
        )

    def test_overlap_matches_custom_date_formats(self):
        # Future Opportunity dates may be DMY/ISO while governed windows are
        # ISO/DMY — overlap must be format-agnostic.
        html = self._render([
            {**self._window("15.06.2026", "15.11.2026"), "start_date": "2026-06-15",
             "end_date": "2026-11-15"},
        ])
        self.assertIn("&middot; <strong>Sade Sati</strong>", html)


@unittest.skipUnless(
    os.path.isfile(RAJU_CANONICAL) and os.path.isfile(RAJU_INDEX),
    "RAJU fixture not available",
)
class TestRajuRealData(unittest.TestCase):
    """Second real horoscope: proves the companion is generic (not MVS-specific)."""

    @classmethod
    def setUpClass(cls):
        from app.pipeline_runner import PipelineRunner
        from app.reports.companion_builder import companion_builder
        from app.reports.companion_html_generator import companion_html_generator

        cls.runner = PipelineRunner()
        cls.companion_builder = companion_builder
        cls.companion_html_generator = companion_html_generator
        with open(RAJU_CANONICAL, encoding="utf-8") as f:
            cls.canon = json.load(f)
        with open(RAJU_INDEX, encoding="utf-8") as f:
            cls.mi = json.load(f)

    def _build(self):
        raw = dict(self.canon)
        raw["_machine_index"] = self.mi
        outputs = self.runner.process(raw)
        return self.companion_builder.build(outputs, self.mi)

    def test_counts_and_dynamic_identity(self):
        payload = self._build()
        self.assertEqual(len(payload["question_catalog"]), 83)
        self.assertEqual(len(payload["question_results"]), 65)
        self.assertEqual(len(payload["question_un_evaluated"]), 18)
        # Distinct identity from the MVS fixtures -> dynamic client derivation.
        self.assertNotEqual(payload["client_profile"].get("name"), "mvs prasad")
        self.assertNotEqual(payload["client_profile"].get("dob"), "")

    def test_html_renders_for_raju(self):
        payload = self._build()
        html = self.companion_html_generator.generate(payload)
        self.assertIn(payload["client_profile"].get("name", ""), html)
        self.assertEqual(html.count("INSUFFICIENT ENGINE DOMAIN COVERAGE"), 18)


class TestCompanionPdfBatchStep(unittest.TestCase):
    """Hermetic: companion PDF generation + the batch driver's write step.

    The batch driver routes the companion HTML string through
    ``PDFGenerator.generate_html`` (same WeasyPrint -> Playwright infra as the
    main report). The renderer itself is stubbed so no browser/PDF engine is
    required; only the add-only wiring introduced for the companion PDF is
    covered here.
    """

    def test_generate_html_renders_verbatim_no_details_forcing(self):
        from app.reports.pdf_generator import PDFGenerator

        generator = PDFGenerator()
        sample_html = "<details><summary>Q</summary><p>Body</p></details>"
        with mock.patch.object(
            PDFGenerator, "_render_html_to_pdf", return_value=b"%PDF-companion"
        ) as renderer:
            result = generator.generate_html(sample_html, client="G Srinivas")
        self.assertEqual(result, b"%PDF-companion")
        # The exact HTML is passed through untouched (no <details open> rewrite).
        renderer.assert_called_once_with(sample_html, "G Srinivas")

    def test_generate_html_defaults_client(self):
        from app.reports.pdf_generator import PDFGenerator

        generator = PDFGenerator()
        with mock.patch.object(
            PDFGenerator, "_render_html_to_pdf", return_value=b"%PDF"
        ) as renderer:
            generator.generate_html("<html></html>")
        renderer.assert_called_once_with("<html></html>", "Vedic-AI Report")

    def test_write_companion_pdf_writes_named_file(self):
        from batch_reports import write_companion_pdf

        class StubPdfGenerator:
            def __init__(self):
                self.received = {}

            def generate_html(self, html_content, client="Vedic-AI Report"):
                self.received = {"html": html_content, "client": client}
                return b"%PDF-batch-companion"

        stub = StubPdfGenerator()
        with tempfile.TemporaryDirectory() as tmp:
            path, pdf = write_companion_pdf(
                stub, "<html>c</html>",
                {"client_profile": {"name": "G Srinivas"}},
                tmp, "g srinivas en",
            )
            self.assertEqual(os.path.basename(path), "g srinivas en_companion.pdf")
            self.assertEqual(pdf, b"%PDF-batch-companion")
            with open(path, "rb") as f:
                self.assertEqual(f.read(), b"%PDF-batch-companion")
        self.assertEqual(stub.received["html"], "<html>c</html>")
        self.assertEqual(stub.received["client"], "G Srinivas")


if __name__ == "__main__":
    unittest.main()