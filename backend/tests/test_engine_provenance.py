import unittest
from app.engines.planet_strength_engine import PlanetStrengthEngine
from app.engines.house_strength_engine import HouseStrengthEngine
from app.engines.master_probability_engine import MasterProbabilityEngine
from app.engines.natal_promise_engine import NatalPromiseEngine
from app.engines.dasha_engine import DashaEngine
from app.engines.transit_engine import TransitEngine
from app.formatters.display_formatter import DisplayFormatter


class TestEngineProvenanceBase(unittest.TestCase):
    """Shared assertions for the TR-001 provenance metadata contract.

    Every formula-owner engine must attach real, deterministic provenance to
    its output metadata (engine name, calibration profile, per-factor
    raw/weight/contribution) so the report trace blocks render engine-known
    facts instead of the legacy "Unknown (v1.0)" / weight-1.0 fallbacks.
    """

    PROVENANCE_KEYS = ("engine", "version", "formula_source", "formula_version",
                       "calibration_profile", "calibration_version", "factors")

    def assert_provenance(self, metadata, engine_name, formula_source):
        for key in self.PROVENANCE_KEYS:
            self.assertIn(key, metadata, f"missing metadata key: {key}")
        self.assertEqual(metadata["engine"], engine_name)
        self.assertEqual(metadata["formula_source"], formula_source)
        self.assertEqual(metadata["calibration_profile"], "v1.0_default")
        self.assertTrue(metadata["version"])
        self.assertTrue(metadata["formula_version"])
        self.assertTrue(metadata["calibration_version"])
        self.assertTrue(metadata["factors"], "factors provenance must not be empty")

    def assert_factor_math(self, factors):
        """raw × weight must equal contribution for every recorded factor."""
        for key, fm in factors.items():
            self.assertAlmostEqual(
                fm["raw"] * fm["weight"], fm["contribution"], places=6,
                msg=f"{key}: raw*weight != contribution",
            )


class TestPlanetEngineProvenance(TestEngineProvenanceBase):
    def setUp(self):
        self.engine = PlanetStrengthEngine()

    def test_planet_engine_emits_provenance(self):
        planet_data = {
            "name": "sun", "dignity": "exalted", "house_type": "kendra",
            "is_combust": False, "is_retrograde": False,
            "benefic_aspects_count": 1, "malefic_aspects_count": 0,
        }
        result = self.engine.calculate_strength(planet_data)
        md = result["metadata"]
        self.assert_provenance(md, "PlanetStrengthEngine", "calibration.planet_strength")
        self.assertEqual(md["factors"]["dignity"]["weight"], 0.25)
        self.assertEqual(md["factors"]["house_placement"]["weight"], 0.20)
        self.assert_factor_math(md["factors"])
        for key, fm in md["factors"].items():
            self.assertAlmostEqual(
                fm["contribution"], result["breakdown"][key], places=6,
                msg=f"{key}: contribution != breakdown",
            )


class TestHouseEngineProvenance(TestEngineProvenanceBase):
    def setUp(self):
        self.engine = HouseStrengthEngine()

    def test_house_engine_emits_provenance(self):
        house_data = {
            "house": "1", "sav_points": 30, "occupants": ["jupiter"],
            "aspected_by": ["venus"], "house_type": "kendra", "lord": "mars",
        }
        result = self.engine.calculate_strength(house_data)
        md = result["metadata"]
        self.assert_provenance(md, "HouseStrengthEngine", "calibration.house_strength")
        self.assertEqual(md["factors"]["sav"]["weight"], 0.30)
        self.assertAlmostEqual(
            md["factors"]["sav"]["contribution"], result["breakdown"]["sav"], places=6
        )
        self.assert_factor_math(md["factors"])


class TestMasterEngineProvenance(TestEngineProvenanceBase):
    def setUp(self):
        self.engine = MasterProbabilityEngine()

    def test_master_engine_emits_provenance(self):
        result = self.engine.evaluate({})
        md = result["metadata"]
        self.assert_provenance(md, "MasterProbabilityEngine", "calibration.master_probability")
        for key, fm in md["factors"].items():
            self.assertEqual(fm["weight"], result["weights"][key])
            self.assertEqual(fm["raw"], result["breakdown"][key])
        total = sum(fm["contribution"] for fm in md["factors"].values())
        self.assertAlmostEqual(total, result["raw_score"], places=3)
        self.assertEqual(result["final_score"], 50)  # all-stub neutral score unchanged


class TestNatalEngineProvenance(TestEngineProvenanceBase):
    def setUp(self):
        self.engine = NatalPromiseEngine()

    def test_natal_engine_emits_provenance_per_domain(self):
        planets = {
            n: {"final_score": 60, "confidence_flags": [], "sign": ""}
            for n in ("venus", "jupiter", "mercury", "saturn", "moon", "mars", "sun", "ketu")
        }
        houses = {str(h): {"final_score": 50} for h in range(1, 13)}
        norm_houses = {str(h): {"lord": "", "occupants": [], "aspected_by": []} for h in range(1, 13)}
        result = self.engine.evaluate(
            planets, houses, {}, {}, {"sav_chart": {}}, {}, norm_houses
        )
        for domain, data in result.items():
            md = data["metadata"]
            self.assert_provenance(md, "NatalPromiseEngine", "calibration.natal_promise")
            self.assertEqual(md["factors"]["bhava"]["weight"], 0.35)
            self.assertEqual(md["factors"]["bhavadhipati"]["weight"], 0.30)
            self.assertEqual(md["factors"]["karaka"]["weight"], 0.20)
            self.assertEqual(md["factors"]["varga"]["weight"], 0.15)
            self.assert_factor_math(md["factors"])


class TestDashaEngineProvenance(TestEngineProvenanceBase):
    def setUp(self):
        self.engine = DashaEngine()

    def test_dasha_engine_emits_provenance(self):
        normalized_data = {
            "dashas": {
                "timeline": [{
                    "mahadasha": "saturn", "antardasha": "jupiter",
                    "pratyantardasha": "venus", "start_date": "2020-01-01",
                }]
            },
            "planets": {"saturn": {"house": 3}, "jupiter": {"house": 5}},
        }
        dependency_scores = {"saturn": {"final_score": 70.0}, "jupiter": {"final_score": 65.0}}
        results = self.engine.evaluate(normalized_data, dependency_scores, target_date="2020-06-01")
        md = results["metadata"]
        self.assert_provenance(md, "DashaEngine", "calibration.dasha")
        self.assertEqual(md["factors"]["mahadasha"]["weight"], 0.50)
        self.assertEqual(md["factors"]["mahadasha"]["raw"], 70.0)
        self.assertEqual(md["factors"]["antardasha"]["weight"], 0.30)
        self.assertEqual(md["factors"]["pratyantardasha"]["weight"], 0.20)
        self.assert_factor_math(md["factors"])


class TestTransitEngineProvenance(TestEngineProvenanceBase):
    def setUp(self):
        self.engine = TransitEngine()

    def test_transit_engine_emits_provenance_on_stub(self):
        result = self.engine.evaluate({}, {}, {}, {}, {})
        md = result["metadata"]
        self.assert_provenance(md, "TransitEngine", "calibration.transit")
        for key, fm in md["factors"].items():
            self.assertEqual(fm["weight"], self.engine.weights[key])
            self.assertEqual(fm["raw"], 50.0)
            self.assertAlmostEqual(fm["raw"] * fm["weight"], fm["contribution"], places=6)
        self.assertEqual(result["activation_score"], 50)


class TestDisplayFormatterProvenance(TestEngineProvenanceBase):
    def test_build_explanation_uses_engine_weights(self):
        """The report trace must render engine-known weights, never weight=1.0."""
        engine = MasterProbabilityEngine()
        master = engine.evaluate({})
        explanation = DisplayFormatter._build_explanation(master, 50, "Executive Synthesis")
        self.assertEqual(explanation.engine_name, "MasterProbabilityEngine")
        self.assertNotEqual(explanation.engine_name, "Unknown")
        self.assertEqual(explanation.formula_source, "calibration.master_probability")
        by_name = {f.factor_name: f for f in explanation.factors}
        self.assertEqual(by_name["natal_promise"].weight, 0.40)
        self.assertEqual(by_name["planet_strength"].weight, 0.15)
        for f in explanation.factors:
            self.assertNotEqual(f.weight, 1.0, f"{f.factor_name} fell back to weight 1.0")

    def test_build_explanation_fallback_unchanged_for_engine_without_provenance(self):
        """Engines without provenance (e.g. YogaEngine) keep the legacy path."""
        explanation = DisplayFormatter._build_explanation({}, 0, "Yoga Detection Only")
        self.assertEqual(explanation.engine_name, "Unknown")
