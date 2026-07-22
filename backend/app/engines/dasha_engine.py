from typing import Dict, Any
from app.config.astrology_constants import DASHA_SCORING_MATRIX
from app.utils.astrology_math import calculate_planetary_axis

class DashaEngine:
    """
    Dasha Engine (Phase 6)
    Evaluates temporal activation based on currently active Vimshottari Dasha lords.
    
    NOTE: This engine does NOT calculate timelines. It assumes the Mahadasha (MD)
    and Antardasha (AD) lords have been extracted from the PDF by the parser.
    It focuses exclusively on relationship analysis and timing multipliers.
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.scoring_matrix = calibration.dasha.get('DASHA_SCORING_MATRIX', {})
        self.calibration = calibration
        try:
            self.weights = calibration.active_profile.get("sections", {}).get("dasha", {}).get("parameters", {}).get("synthesis_weights", {}).get("current_value", {})
        except (KeyError, TypeError):
            self.weights = {}

    def _get_weight(self, param_name: str, default: float) -> float:
        # Note: synthesis_weights is a dict of floats, not the standard weight_pct schema
        return float(self.weights.get(param_name, default))

    def evaluate(self, normalized_data: Dict[str, Any], dependency_scores: Dict[str, Any] = None, target_date: str = None) -> Dict[str, Any]:
        """
        Evaluates the timing multipliers for the currently active Dasha lords.
        """
        import datetime
        if target_date is None:
            target_date = datetime.date.today().strftime('%Y-%m-%d')
            
        if dependency_scores is None:
            dependency_scores = {}

        results = {}
        dashas = normalized_data.get("dashas", {})
        timeline = dashas.get("timeline", [])
        
        # If the parser hasn't extracted a timeline, return an empty evaluation
        if not timeline:
            return results
            
        # Filter out rows with unparseable dates to prevent strptime crashes
        clean_timeline = []
        for x in timeline:
            try:
                datetime.datetime.strptime(x.get('start_date', ''), '%Y-%m-%d')
                clean_timeline.append(x)
            except ValueError:
                pass
                
        timeline = clean_timeline
        if not timeline:
            return results
            
        # Sort timeline chronologically
        timeline.sort(key=lambda x: datetime.datetime.strptime(x['start_date'], '%Y-%m-%d'))
            
        target_dt = datetime.datetime.strptime(target_date, '%Y-%m-%d')
        active_record = None
        
        for i in range(len(timeline)):
            d1 = datetime.datetime.strptime(timeline[i]['start_date'], '%Y-%m-%d')
            if i < len(timeline) - 1:
                d2 = datetime.datetime.strptime(timeline[i+1]['start_date'], '%Y-%m-%d')
                if d1 <= target_dt < d2:
                    active_record = timeline[i]
                    break
            else:
                if d1 <= target_dt:
                    active_record = timeline[i]
                    break
                    
        if not active_record:
            return results

        md_lord = active_record.get("mahadasha", "unknown").lower()
        ad_lord = active_record.get("antardasha", "unknown").lower()
        pd_lord = active_record.get("pratyantardasha", "unknown").lower()

        planets = normalized_data.get("planets", {})
        md_planet_data = planets.get(md_lord, {})
        ad_planet_data = planets.get(ad_lord, {})
        # Note: We can also compute axis for PD if we wanted, but currently focusing on MD/AD axis
        pd_planet_data = planets.get(pd_lord, {})

        # Calculate the astrological axis (relationship) between MD and AD lords
        relationship_key = calculate_planetary_axis(
            md_planet_data.get("house", 1),
            ad_planet_data.get("house", 1)
        )

        relationship_multiplier = self.scoring_matrix.get("relationship_scalars", {}).get(relationship_key, 1.0)

        # Generate results for MD Lord
        md_base_score = dependency_scores.get(md_lord, {}).get("final_score", 0.0)
        results[md_lord] = self._build_dasha_payload(
            md_lord, md_base_score, "mahadasha", relationship_multiplier, relationship_key
        )

        # Generate results for AD Lord
        ad_base_score = dependency_scores.get(ad_lord, {}).get("final_score", 0.0)
        results[ad_lord] = self._build_dasha_payload(
            ad_lord, ad_base_score, "antardasha", relationship_multiplier, relationship_key
        )
        
        # Generate results for PD Lord
        pd_base_score = dependency_scores.get(pd_lord, {}).get("final_score", 0.0)
        results[pd_lord] = self._build_dasha_payload(
            pd_lord, pd_base_score, "pratyantardasha", 1.0, "1_1" # PD doesn't use the multiplier in legacy
        )
        
        # Calculate aggregated dasha strength
        dasha_strength = (md_base_score * self._get_weight("md", 0.50)) + (ad_base_score * self._get_weight("ad", 0.30)) + (pd_base_score * self._get_weight("pd", 0.20))
        dasha_strength = max(0.0, min(100.0, dasha_strength))
        
        # Active index
        active_idx = timeline.index(active_record)

        # PD Dates
        pd_start = active_record.get("start_date")
        pd_end = timeline[active_idx + 1].get("start_date") if active_idx + 1 < len(timeline) else "Unknown"

        # AD Dates
        ad_start = None
        for i in range(active_idx, -1, -1):
            if timeline[i].get("mahadasha", "").lower() != md_lord or timeline[i].get("antardasha", "").lower() != ad_lord:
                break
            ad_start = timeline[i].get("start_date")

        ad_end = "Unknown"
        for i in range(active_idx + 1, len(timeline)):
            if timeline[i].get("mahadasha", "").lower() != md_lord or timeline[i].get("antardasha", "").lower() != ad_lord:
                ad_end = timeline[i].get("start_date")
                break

        # MD Dates
        md_start = None
        for i in range(active_idx, -1, -1):
            if timeline[i].get("mahadasha", "").lower() != md_lord:
                break
            md_start = timeline[i].get("start_date")

        md_end = "Unknown"
        for i in range(active_idx + 1, len(timeline)):
            if timeline[i].get("mahadasha", "").lower() != md_lord:
                md_end = timeline[i].get("start_date")
                break

        # Build synthesis
        results["synthesis"] = {
            "active_md": md_lord,
            "md_start": md_start,
            "md_end": md_end,
            "active_ad": ad_lord,
            "ad_start": ad_start,
            "ad_end": ad_end,
            "active_pd": pd_lord,
            "pd_start": pd_start,
            "pd_end": pd_end,
            "md_strength": md_base_score,
            "ad_strength": ad_base_score,
            "pd_strength": pd_base_score,
            "dasha_strength": round(dasha_strength, 2),
            "target_date": target_date
        }
        
        # Preserve full timeline for UI transparency layer
        for i, record in enumerate(timeline):
            md = record.get("mahadasha", "unknown").lower()
            ad = record.get("antardasha", "unknown").lower()
            pd = record.get("pratyantardasha", "unknown").lower()
            
            md_s = dependency_scores.get(md, {}).get("final_score", 0.0)
            ad_s = dependency_scores.get(ad, {}).get("final_score", 0.0)
            pd_s = dependency_scores.get(pd, {}).get("final_score", 0.0)
            
            record["md_planet_strength"] = md_s
            record["ad_planet_strength"] = ad_s
            record["pd_planet_strength"] = pd_s
            
            d_str = (md_s * self._get_weight("md", 0.50)) + (ad_s * self._get_weight("ad", 0.30)) + (pd_s * self._get_weight("pd", 0.20))
            record["dasha_activation"] = round(max(0.0, min(100.0, d_str)), 2)
            
            if i + 1 < len(timeline):
                record["end_date"] = timeline[i+1].get("start_date")
            else:
                record["end_date"] = "Unknown"
            
        results["timeline"] = timeline

        return results

    def _build_dasha_payload(self, entity_id: str, base_score: float, level: str, multiplier: float, axis: str) -> Dict[str, Any]:
        """Constructs the standard JSON contract with temporal activation populated."""
        return {
            "metadata": {
                "entity_id": entity_id,
                "entity_type": "planet"
            },
            "final_score": base_score, # Immutable D1 Rule
            "breakdown": {},
            "modifiers": {},
            "temporal_activation": {
                "active_dasha_level": level,
                "timing_multiplier": multiplier
            },
            "confidence_flags": [f"active_{level}", f"dasha_axis_{axis}"]
        }