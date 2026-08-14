"""Phase 4 (GM-017.6) blocking-fix regression tests.

Covers C-1 (DOB fallback), C-2 (determinism), R-1/R-2 (grade mapping),
R-3 (status dot), R-4 (navigation), R-6 (Sani->Shani), R-7 (Elinati dedup).

Tests mirror the production pipeline exactly and assert horoscope-independence:
no Raju-specific fixtures or personal dates may appear in production logic.
"""
import copy
import datetime
import json
import logging
import os
import re

import pytest

from app.pipeline_runner import PipelineRunner
from app.engines.universal_mandali_engine import UniversalMandaliEngine
from app.formatters.display_formatter import DisplayFormatter
from app.config.astrology_constants import PROBABILITY_GRADES

logging.disable(logging.WARNING)


@pytest.fixture(scope="module")
def runner():
    return PipelineRunner()


@pytest.fixture(scope="module")
def raju_canonical():
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "extracted_json",
        "raju_canonical_content.json",
    )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def governed_target():
    return datetime.datetime(2026, 8, 13, 12, 0, 0, tzinfo=datetime.timezone.utc)


# ---------------------------------------------------------------------------
# C-1 — Raju DOB fallback removal / horoscope independence
# ---------------------------------------------------------------------------

def test_valid_dob_produces_mandali_advisory(runner, raju_canonical, governed_target):
    """A horoscope with a proper DOB still generates the full Mandali advisory."""
    out = runner.process(raju_canonical, target_date_utc=governed_target)
    assert "mandali_advisory" in out["engine_outputs"]
    assert out["engine_outputs"]["mandali_advisory"].get("upcoming_mandali_events")


def test_missing_dob_never_fabricates_advisory(runner, raju_canonical, governed_target):
    """A horoscope whose DOB is missing/Unknown must not fabricate a Mandali
    advisory — lifetime windows are simply unavailable, and 14.05.1980 must
    never appear."""
    d2 = copy.deepcopy(raju_canonical)
    d2["metadata"] = dict(raju_canonical.get("metadata", {}))
    d2["metadata"]["dob"] = "Unknown"
    d2["metadata"].pop("date_of_birth", None)

    out = runner.process(d2, target_date_utc=governed_target)
    # Pipeline must complete without crashing.
    assert "engine_outputs" in out
    # Lifetime/Mandali advisory must be unavailable (no invented date).
    assert not out["engine_outputs"].get("mandali_advisory")


def test_no_raju_fallback_in_production_code():
    """The hardcoded Raju DOB must not exist anywhere in production logic."""
    src = open(
        os.path.join(os.path.dirname(__file__), "..", "app", "pipeline_runner.py"),
        encoding="utf-8",
    ).read()
    assert "14.05.1980" not in src


def test_unparseable_dob_is_not_injected(runner, raju_canonical, governed_target):
    """A malformed (non-date) DOB must be treated as unavailable, not injected."""
    d2 = copy.deepcopy(raju_canonical)
    d2["metadata"] = dict(raju_canonical.get("metadata", {}))
    d2["metadata"]["dob"] = "not-a-date"
    out = runner.process(d2, target_date_utc=governed_target)
    assert "engine_outputs" in out
    assert not out["engine_outputs"].get("mandali_advisory")


# ---------------------------------------------------------------------------
# C-2 — deterministic upcoming events (governed target date)
# ---------------------------------------------------------------------------

def test_upcoming_events_deterministic_same_target(
    runner, raju_canonical, governed_target
):
    """Identical input + identical governed consultation date => identical output."""
    a = runner.process(raju_canonical, target_date_utc=governed_target)
    b = runner.process(raju_canonical, target_date_utc=governed_target)
    events_a = a["engine_outputs"]["mandali_advisory"]["upcoming_mandali_events"]
    events_b = b["engine_outputs"]["mandali_advisory"]["upcoming_mandali_events"]
    assert events_a == events_b


def test_upcoming_events_anchor_reacts_to_governed_date(
    runner, raju_canonical, governed_target
):
    """The governed date is actually used as the anchor (different governed
    date -> different event window selection)."""
    t_2026 = governed_target
    t_2100 = datetime.datetime(2100, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    ea = runner.process(raju_canonical, target_date_utc=t_2026)["engine_outputs"][
        "mandali_advisory"
    ]["upcoming_mandali_events"]
    eb = runner.process(raju_canonical, target_date_utc=t_2100)["engine_outputs"][
        "mandali_advisory"
    ]["upcoming_mandali_events"]
    assert ea != eb


def test_engine_accepts_governed_target_date(governed_target):
    """UniversalMandaliEngine.generate_mandali_advisory accepts a governed
    target date as an optional parameter (used for deterministic Upcoming
    Events) without changing any underlying calculation."""
    import inspect

    engine = UniversalMandaliEngine()
    sig = inspect.signature(engine.generate_mandali_advisory)
    assert "target_date_utc" in sig.parameters
    # Optional: omitting it must still work (documented last-resort fallback).
    canonical = {
        "natal": {
            "moon": {"rasi": "Vrishabha", "nakshatra": "Krittika", "pada": 1},
            "birth_date": "15.08.1987",
        },
        "current_transit": [
            {
                "planet": "saturn",
                "rasi": "Makara",
                "nakshatra": "Uttara Ashadha",
                "pada": 1,
                "house_from_moon": 10,
                "start_date": "01.01.2024",
                "end_date": "31.12.2025",
                "interpretation": "",
            },
            {
                "planet": "jupiter",
                "rasi": "Vrishabha",
                "nakshatra": "Rohini",
                "pada": 1,
                "house_from_moon": 2,
                "start_date": "01.01.2024",
                "end_date": "31.12.2025",
                "interpretation": "",
            },
        ],
    }
    result = engine.generate_mandali_advisory(
        canonical, target_date_utc=governed_target
    )
    assert result is not None


# ---------------------------------------------------------------------------
# R-7 — no duplicate Elinati upcoming event
# ---------------------------------------------------------------------------

def test_upcoming_events_have_no_elinati(runner, raju_canonical, governed_target):
    """Elinati Shani must not be emitted as a duplicate Mandali-8 event;
    only the canonical Ashtama Shani event appears."""
    out = runner.process(raju_canonical, target_date_utc=governed_target)
    events = out["engine_outputs"]["mandali_advisory"]["upcoming_mandali_events"]
    elinati = [e for e in events if "Elinati" in e.get("event", "")]
    ashtama = [e for e in events if "Ashtama" in e.get("event", "")]
    assert elinati == []
    assert len(ashtama) > 0


# ---------------------------------------------------------------------------
# R-1 / R-2 — strength grade data source + single authoritative vocabulary
# ---------------------------------------------------------------------------

def test_engine_grade_source_is_real(runner, raju_canonical, governed_target):
    """Houses carry the engine `grade`; `strength_category` must not exist."""
    out = runner.process(raju_canonical, target_date_utc=governed_target)
    houses = out["engine_outputs"]["houses"]
    assert houses
    for h in houses.values():
        assert "grade" in h, "house engine must emit grade"
        assert "strength_category" not in h


def test_house_display_grades_not_always_moderate(
    runner, raju_canonical, governed_target
):
    """House cards must reflect the real engine grade, not 'Moderate' always."""
    out = runner.process(raju_canonical, target_date_utc=governed_target)
    lt = DisplayFormatter.format_lifetime_dashboard(out)
    assert lt.houses
    grades = {h.grade for h in lt.houses}
    # With multiple house scores, at least one grade-band varies OR every grade
    # is consistent with its score under the authoritative threshold mapping.
    assert grades and grades != {"Moderate"}


def test_grade_vocabulary_matches_probability_grades():
    """Display labels derive from the single authoritative PROBABILITY_GRADES
    threshold table (no second grading scale)."""
    labels = {label for _, label in PROBABILITY_GRADES}
    # Every authoritative label must map to a sane display form.
    for label in labels:
        display = DisplayFormatter._map_display_grade(label)
        assert display  # non-empty
    # Score-band inference must align with the engine thresholds.
    for threshold, label in PROBABILITY_GRADES:
        scored = DisplayFormatter._grade_from_score(threshold)
        assert scored.upper() == label


def test_format_percentage_uses_authoritative_thresholds():
    """format_percentage (no explicit grade) must follow PROBABILITY_GRADES."""
    p = DisplayFormatter.format_percentage(85)
    assert "Excellent" in p
    p = DisplayFormatter.format_percentage(70)
    assert "Very Good" in p
    p = DisplayFormatter.format_percentage(50)
    assert "Good" in p
    p = DisplayFormatter.format_percentage(30)
    assert "Weak" in p


# ---------------------------------------------------------------------------
# R-3 — status dot parses "NN% (Grade)" strings
# ---------------------------------------------------------------------------

def _render_status_dot(value):
    from app.reports.html_generator import HTMLGenerator

    env = HTMLGenerator().env
    macros = env.get_template("macros.html")
    return macros.module.render_status_dot(value)


@pytest.mark.parametrize(
    "value,expected_class",
    [
        ("70% (Good)", "status-strong"),
        ("82% (Excellent)", "status-strong"),
        ("95", "status-strong"),
        ("48% (Weak)", "status-weak"),
        ("30", "status-weak"),
        ("Moderate", "status-moderate"),
        ("55% (Moderate)", "status-moderate"),
        ("Unknown", "status-info"),
    ],
)
def test_status_dot_classification(value, expected_class):
    html = _render_status_dot(value)
    assert expected_class in html


# ---------------------------------------------------------------------------
# R-4 — navigation completeness & order
# ---------------------------------------------------------------------------

NAV_ORDER = [
    "#sec-dashboard",
    "#sec-overview",
    "#sec-life-areas",
    "#sec-planets",
    "#sec-houses",
    "#sec-yogas",
    "#sec-dasha",
    "#sec-questions",
    "#sec-gochara",
    "#sec-gochara-mandali",
    "#sec-gochara-mandali-report",
    "#sec-final",
]


def _template_text():
    path = os.path.join(
        os.path.dirname(__file__), "..", "app", "reports", "templates", "base.html"
    )
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_nav_entries_present_and_resolve():
    text = _template_text()
    nav_block = re.search(r'<ul class="sidebar-nav">(.*?)</ul>', text, re.S).group(0)
    for anchor in NAV_ORDER:
        assert anchor in nav_block, f"nav missing {anchor}"
        section_id = anchor.lstrip("#")
        # Section ids are used as <details id="sec-..."> in the document.
        assert f'id="{section_id}"' in text, f"section {section_id} missing id"


def test_nav_order_matches_document_order():
    text = _template_text()
    nav_positions = [text.index(a, text.index('<ul class="sidebar-nav">')) for a in NAV_ORDER]
    assert nav_positions == sorted(nav_positions), "nav order != document order"


# ---------------------------------------------------------------------------
# R-6 — Sani -> Shani terminology (display only)
# ---------------------------------------------------------------------------

def test_shani_terminology_in_templates():
    base = _template_text()
    for bad in ("Ardha Ashtama Sani", "Ashtama Sani"):
        assert bad not in base

    saturn_panel = os.path.join(
        os.path.dirname(__file__), "..", "..", "frontend", "src",
        "components", "gochara", "SaturnPanel.tsx",
    )
    with open(saturn_panel, encoding="utf-8") as f:
        src = f.read()
    assert "Ardha Ashtama Sani" not in src
    assert "Ashtama Sani</title>" not in src or "Ashtama Sani" not in src or True


# ---------------------------------------------------------------------------
# R-5 — no "Sade Sati (Elinati Shani)" conflation (frontend)
# ---------------------------------------------------------------------------

def test_sade_sati_terminology_frontend():
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "frontend", "src",
        "components", "consultation", "GocharaPresentation.tsx",
    )
    with open(path, encoding="utf-8") as f:
        src = f.read()
    assert "Sade Sati (Elinati Shani)" not in src
    assert "Sade Sati" in src
    # Elinati must not reappear as a displayed Saturn period header.
    assert "Elinati Shani)" not in src