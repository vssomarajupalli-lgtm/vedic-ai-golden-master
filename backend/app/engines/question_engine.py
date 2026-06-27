"""
QuestionEngine — Deterministic domain routing and probability synthesis.

Architecture:
    Question (str)
        ↓
    Domain Router (keyword matching)
        ↓
    Returns domain to PipelineRunner (orchestrator)
        ↓
    PipelineRunner passes explicit components back to QuestionEngine
        ↓
    Structured answer: probability, grade, timing_confidence, domain

Rules:
    - Zero AI/ML. Pure keyword lookup for routing.
    - Domain routing is keyword-prefix, not semantic matching.
    - If no domain match: returns multi-domain summary (generic answer).
    - QuestionEngine MUST NOT instantiate or call MasterProbabilityEngine (DR-007).
    - QuestionEngine must NOT collapse components (DR-008).
"""
from app.config.astrology_constants import NATAL_PROMISE_GRADES, PROBABILITY_GRADES

# ---------------------------------------------------------------------------
# Domain Keyword Routing Table
# ---------------------------------------------------------------------------
DOMAIN_KEYWORDS = {
    "marriage":    [
        "marriage", "married", "wedding", "spouse", "husband", "wife",
        "partner", "love", "relationship", "divorce", "remarriage", "second marriage"
    ],
    "career":      [
        "career", "job", "profession", "work", "business", "promotion",
        "employment", "office", "salary", "transfer",
        "foreign job", "government job", "service"
    ],
    "wealth":      [
        "wealth", "money", "finance", "rich", "income", "earn",
        "financial", "investment", "profit", "loss", "debt", "loan",
        "lottery", "inheritance", "windfall"
    ],
    "education":   [
        "education", "study abroad", "study", "school", "college", "university",
        "degree", "learning", "knowledge", "exam", "course", "graduate",
        "higher education", "academic"
    ],
    "children":    [
        "children", "child", "baby", "son", "daughter", "pregnancy",
        "offspring", "progeny", "birth", "kid", "kids", "parent", "parenthood"
    ],
    "property":    [
        "property", "house", "home", "land", "real estate", "apartment",
        "flat", "plot", "building", "construction", "own house"
    ],
    "health":      [
        "health", "illness", "disease", "medical", "sick", "wellness",
        "body", "surgery", "hospital", "accident", "injury", "recover",
        "longevity", "chronic"
    ],
    "spirituality":[
        "spiritual", "religion", "dharma", "moksha", "meditation",
        "yoga", "divine", "pilgrimage", "temple", "renunciation"
    ],
}

# Priority order: first match wins when multiple domains could match
DOMAIN_PRIORITY = [
    "marriage", "career", "wealth", "children", "education",
    "property", "health", "spirituality"
]


class QuestionEngine:
    """
    Deterministic question router and response composer.

    Usage:
        engine = QuestionEngine()
        domain = engine.route_domain("Will I get married?")
        # orchestrator gathers components
        answer = engine.compose_response(...)

    Returns a structured answer dict with domain, probability score, grade,
    natal promise, dasha confidence, and transit evidence.
    """

    def __init__(self, calibration=None):
        if calibration is None:
            from app.calibration.calibration_manager import CalibrationManager
            calibration = CalibrationManager()
        self.keywords        = DOMAIN_KEYWORDS
        self.priority        = DOMAIN_PRIORITY
        self.promise_grades  = calibration.natal_promise.get('NATAL_PROMISE_GRADES', [])

    # -------------------------------------------------------------------------
    # Public Interface
    # -------------------------------------------------------------------------

    def route_domain(self, question: str) -> str | None:
        """
        Keyword-based domain routing.
        Scans the question (lowercased) for each domain's keywords.
        Returns the first matched domain in DOMAIN_PRIORITY order.
        Returns None if no domain matches.
        """
        q = question.lower().strip()
        for domain in self.priority:
            for keyword in self.keywords[domain]:
                if keyword in q:
                    return domain
        return None

    def compose_response(
        self,
        question: str,
        domain: str | None,
        natal_promise: dict,
        dasha_activation: dict,
        transit_activation: dict,
        final_probability: dict,
        bav_timing_confidence: str = "UNKNOWN",
        yogas: dict = None
    ) -> dict:
        """
        Takes separated domain components from the orchestrator and composes the final 
        response dict without performing any recalculation or collapsing layers.
        
        Args:
            question (str): Free-text question from the user.
            domain (str | None): The routed domain.
            natal_promise (dict): The specific domain promise block.
            dasha_activation (dict): The dasha engine outputs.
            transit_activation (dict): The transit engine outputs.
            final_probability (dict): The master probability block re-calculated for this domain.
            bav_timing_confidence (str): Ashtakavarga confidence string.
            yogas (dict): Detected yogas.
            
        Returns:
            dict: Structured answer with probability, grade, and separated components.
        """
        routed = bool(domain)
        natal_score = natal_promise.get("score", 50.0)

        # Step 1: Extract dasha timing evidence
        synthesis = dasha_activation.get("synthesis", {})
        active_md = synthesis.get("active_md", "unknown")
        active_ad = synthesis.get("active_ad", "unknown")
        active_pd = synthesis.get("active_pd", "unknown")
        dasha_strength = synthesis.get("dasha_strength", 50.0)

        timing = {
            "mahadasha": active_md,
            "antardasha": active_ad,
            "pratyantardasha": active_pd,
            "dasha_strength": dasha_strength,
            "bav_timing_confidence": bav_timing_confidence,
            "activation_level": self._activation_label(dasha_strength / 50.0),
        }

        # Step 2: Extract transit evidence
        transit_score = transit_activation.get("activation_score", 50.0)

        # Step 3: Compose text
        prob_score = final_probability.get("final_score", 50)
        prob_grade = final_probability.get("grade", "UNKNOWN")
        promise    = self._promise_grade(natal_score)

        if not routed:
            answer_text = (
                f"Domain could not be determined from: '{question}'. "
                f"General probability: {prob_score}/100 ({prob_grade}). "
                f"Active dasha: {active_md.capitalize()} MD / {active_ad.capitalize()} AD / {active_pd.capitalize()} PD."
            )
        else:
            domain_label = domain.capitalize()
            lines = [
                f"{domain_label} promise from natal chart: {natal_score}/100 ({promise}).",
                f"Combined probability: {prob_score}/100 ({prob_grade}).",
                f"Active dasha: {active_md.capitalize()} Mahadasha / {active_ad.capitalize()} Antardasha / {active_pd.capitalize()} Pratyantardasha.",
                f"Dasha strength: {dasha_strength}/100 (level: {timing['activation_level']}).",
                f"Ashtakavarga timing confidence: {bav_timing_confidence.upper()}.",
                f"Transit activation score: {transit_score}/100."
            ]
            answer_text = " ".join(lines)

        # Step 4: Extract Top Future Opportunities (from MasterProbabilityEngine projection)
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        
        lifetime_projection = final_probability.get("lifetime_projection", [])
        future_opps = []
        for record in lifetime_projection:
            start_date = record.get("start_date", "1900-01-01")
            if start_date >= now:
                future_opps.append({
                    "period": f"{start_date} to {record.get('end_date', 'Unknown')}",
                    "activation_pct": record.get("activation_pct", 50.0),
                    "final_probability_pct": record.get("final_probability_pct", 50.0),
                    "grade": record.get("grade", "UNKNOWN"),
                    "md": record.get("md", "unknown"),
                    "ad": record.get("ad", "unknown"),
                    "pd": record.get("pd", "unknown")
                })
        
        future_opps.sort(key=lambda x: x["final_probability_pct"], reverse=True)
        top_opportunities = future_opps[:5]

        return {
            "question":      question,
            "domain":        domain,
            "routed":        routed,
            "probability": {
                "score": prob_score,
                "grade": prob_grade,
                "raw":   final_probability.get("raw_score", 50.0),
            },
            "natal_promise": {
                "score":    natal_score,
                "promise":  promise,
                "karaka":   natal_promise.get("karaka", ""),
                "afflictions": natal_promise.get("afflictions", []),
            },
            "timing": timing,
            "transit": {
                "activation_score": transit_score
            },
            "yogas": yogas or {},
            "factor_breakdown": final_probability.get("breakdown", {}),
            "top_opportunities": top_opportunities,
            "answer_text": answer_text,
        }

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _activation_label(multiplier: float) -> str:
        """Maps timing_multiplier to a human-readable activation level."""
        if multiplier >= 1.20:  return "HIGH"
        if multiplier >= 1.10:  return "MODERATE"
        if multiplier >= 1.00:  return "NEUTRAL"
        return "SUPPRESSED"

    def _promise_grade(self, score: float) -> str:
        """4-tier promise classification."""
        for threshold, label in self.promise_grades:
            if score >= threshold:
                return label
        return "PRESENT"
