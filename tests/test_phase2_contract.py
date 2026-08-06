import pytest
import json
from pathlib import Path
import copy
from dataclasses import fields

from app.engines.universal_mandali_engine import (
    UniversalMandaliEngine,
    MandaliAdvisory,
    TransitMandaliPosition,
)

@pytest.fixture(scope="module")
def sample_canonical():
    """Loads a sample canonical JSON file for testing."""
    path = Path(__file__).parent / "data" / "sample_canonical.json"
    with open(path, "r") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def mandali_engine():
    """Provides a singleton instance of the UniversalMandaliEngine."""
    return UniversalMandaliEngine()

@pytest.fixture(scope="module")
def advisory(mandali_engine, sample_canonical):
    """Generates a single advisory object for use in multiple tests."""
    return mandali_engine.generate_mandali_advisory(sample_canonical)

def test_transit_output_contract_schema(advisory):
    """Verifies the final, flat 14-field contract for TransitMandaliPosition."""
    expected_fields = {
        "planet_id", "planet_name", "rasi_id", "rasi_name",
        "nakshatra_id", "nakshatra_name", "pada", "absolute_pada",
        "mandali_number", "mandali_name", "house_from_moon_classical",
        "house_from_moon_mandali", "status", "interpretation_key"
    }
    
    # Get fields from the dataclass definition
    actual_fields = {f.name for f in fields(TransitMandaliPosition)}
    
    assert actual_fields == expected_fields, "TransitMandaliPosition schema mismatch"
    assert len(actual_fields) == 14, "Expected exactly 14 fields in the contract"

    # Check an actual instance from the output
    jupiter_position = advisory.current_transit_mandali.get("jupiter")
    assert jupiter_position is not None
    assert all(hasattr(jupiter_position, field) for field in expected_fields)

def test_mandali_name_formatting(advisory):
    """Verifies that all Mandali names follow the '<Rasi Name> Rasi Mandali' format."""
    # Check CurrentMandali
    assert "Rasi Mandali" in advisory.current_mandali.name
    assert advisory.current_mandali.name == "Makara Rasi Mandali"

    # Check a sample from transit positions
    jupiter_position = advisory.current_transit_mandali.get("jupiter")
    assert "Rasi Mandali" in jupiter_position.mandali_name
    assert jupiter_position.mandali_name == "Meena Rasi Mandali"

def test_planet_placement_completeness_and_uniqueness(advisory, sample_canonical):
    """Verifies that every planet appears exactly once."""
    input_planets = {p["planet"].lower() for p in sample_canonical["current_transit"]}
    output_planets = set(advisory.current_transit_mandali.keys())
    
    assert input_planets == output_planets, "Mismatch between input and output planets"
    assert len(output_planets) == len(input_planets), "Number of placed planets does not match input"

def test_deterministic_and_client_independent(mandali_engine, sample_canonical):
    """
    Tests that identical inputs produce identical outputs and that different
    Canonical JSON inputs produce different, correct Mandali grids automatically.
    """
    canonical_A = sample_canonical
    canonical_B = copy.deepcopy(sample_canonical)
    canonical_B["natal"]["moon"].update({"nakshatra": "Ashwini", "pada": 1, "rasi": "Mesha"})

    advisory_A = mandali_engine.generate_mandali_advisory(canonical_A)
    advisory_B = mandali_engine.generate_mandali_advisory(canonical_B)
    advisory_A_again = mandali_engine.generate_mandali_advisory(canonical_A)

    assert advisory_A != advisory_B, "Different inputs should produce different advisories"
    assert advisory_A == advisory_A_again, "Identical inputs must produce identical advisories"

    jupiter_A = advisory_A.current_transit_mandali.get("jupiter")
    jupiter_B = advisory_B.current_transit_mandali.get("jupiter")
    
    assert jupiter_A.mandali_number == 3
    assert jupiter_B.mandali_number == 1
    assert jupiter_A.mandali_name == "Meena Rasi Mandali"
    assert jupiter_B.mandali_name == "Mesha Rasi Mandali"
