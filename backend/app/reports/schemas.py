from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

# --- Base Schema Component ---
class ClientProfile(BaseModel):
    name: str = "Unknown"
    dob: str = "Unknown"
    tob: str = "Unknown"
    pob: str = "Unknown"
    latitude: float = 0.0
    longitude: float = 0.0
    timezone: str = "UTC"
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# --- Deterministic Reporting Foundations ---
class CalculationFactor(BaseModel):
    factor_name: str
    formula: str = ""
    raw_value: float = 0.0
    weight: float = 0.0
    calibration_key: str = ""
    calibration_value: float = 0.0
    contribution: float = 0.0
    running_total: float = 0.0
    remarks: str = ""

class DeterministicExplanation(BaseModel):
    engine_name: str = ""
    engine_version: str = ""
    formula_source: str = ""
    formula_version: str = ""
    calibration_profile: str = ""
    calibration_version: str = ""
    execution_timestamp: str = ""
    formula: str = ""
    intermediate_calculations: Dict[str, Any] = Field(default_factory=dict)
    factors: List[CalculationFactor] = Field(default_factory=list)
    final_percentage: float = 0.0

# --- SECTION A: Executive Summary ---
class GlobalExecutiveSummaryDisplay(BaseModel):
    overall_score: int
    overall_grade: str
    overall_promise: str
    current_mahadasha: str
    current_antardasha: str
    current_pratyantardasha: str
    current_dasha_remaining: str
    overall_lifetime_trend: str
    strongest_life_area: str
    weakest_life_area: str
    best_planet: str
    weak_planet: str
    best_house: str
    weak_house: str
    upcoming_major_turning_point: str
    present_yogas: List[str] = Field(default_factory=list)
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

# --- SECTION B: Lifetime Horoscope Snapshot ---
class LifetimeSnapshotDisplay(BaseModel):
    overall_promise: str
    current_trend: str
    current_opportunity: str
    current_challenge: str
    current_dasha: str
    best_future_period: str
    current_activation: str
    current_grade: str

# --- SECTION C: Life Area Intelligence ---
class LifeAreaIntelligenceDisplay(BaseModel):
    domain_name: str
    promise_percentage: int
    grade: str
    strengths: List[str]
    weaknesses: List[str]
    supporting_houses: List[str]
    supporting_planets: List[str]
    supporting_yogas: List[str]
    current_dasha_influence: str
    long_term_outlook: str
    attention_factors: List[str]
    interpretation: str
    recommendations: List[str]
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

# --- SECTION D: Planet Intelligence ---
class PlanetIntelligenceDisplay(BaseModel):
    planet_name: str
    strength_score: int
    functional_nature: str
    dignity: str
    lordship: List[str]
    occupation: str
    positive_contributions: List[str]
    negative_contributions: List[str]
    life_themes: List[str]
    supporting_yogas: List[str]
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

# --- SECTION E: House Intelligence ---
class HouseIntelligenceDisplay(BaseModel):
    house_name: str
    score: int
    grade: str
    lord: str
    occupants: List[str]
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

# --- SECTION F: Yoga Intelligence ---
class YogaIntelligenceDisplay(BaseModel):
    yoga_name: str
    status: str
    strength: int
    meaning: str
    supporting_area: str
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

# --- SECTION G: Current Dasha Status ---
class CurrentDashaStatusDisplay(BaseModel):
    current_md: str
    current_ad: str
    current_pd: str
    remaining_duration: str
    current_activation: str
    current_probability: int
    current_grade: str
    interpretation: str
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

# --- SECTION H: Lifetime Timeline ---
class DashaTimelineRowDisplay(BaseModel):
    age: int
    start_date: str
    end_date: str
    md: str
    ad: str
    pd: str
    md_strength: int
    ad_strength: int
    pd_strength: int
    activation_percentage: int
    probability_percentage: int
    grade: str

class LifetimeIntelligenceDashboard(BaseModel):
    snapshot: LifetimeSnapshotDisplay
    life_areas: List[LifeAreaIntelligenceDisplay]
    planets: List[PlanetIntelligenceDisplay]
    houses: List[HouseIntelligenceDisplay]
    yogas: List[YogaIntelligenceDisplay]
    current_dasha_status: CurrentDashaStatusDisplay
    timeline: List[DashaTimelineRowDisplay]

# --- SECTION I: Question Engine Intelligence ---
class QuestionEngineReport(BaseModel):
    question_id: str
    question: str
    domain: str
    final_probability: int
    confidence: float
    explanation: DeterministicExplanation

# --- SECTION J: Gochara (Transit) Intelligence ---
class MandaliReport(BaseModel):
    current_mandali: str = ""
    reference_moon: str = ""
    mandali_number: int = 0
    mandali_boundaries: str = ""
    sade_sati_status: str = "Not Active"
    sade_sati_phase: str = "N/A"
    activated_zones: List[str] = Field(default_factory=list)
    activated_bhavas: List[int] = Field(default_factory=list)
    activated_planets: List[str] = Field(default_factory=list)
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)

class GocharaReport(BaseModel):
    current_transit_date: str = ""
    transit_planets: List[str] = Field(default_factory=list)
    transit_houses: List[int] = Field(default_factory=list)
    transit_strength: int = 0
    activated_houses: List[int] = Field(default_factory=list)
    activated_planets: List[str] = Field(default_factory=list)
    activated_yogas: List[str] = Field(default_factory=list)
    activated_questions: List[str] = Field(default_factory=list)
    explanation: DeterministicExplanation = Field(default_factory=DeterministicExplanation)
    mandali: Optional[MandaliReport] = None

# --- Final Output Schema ---
class FinalReportSchema(BaseModel):
    report_version: str = "1.2.0"
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    client_profile: ClientProfile = Field(default_factory=ClientProfile)
    
    # Section A
    executive_summary: GlobalExecutiveSummaryDisplay
    
    # Section B to H
    lifetime_intelligence: LifetimeIntelligenceDashboard
    
    # Section I (Question Intelligence)
    question_responses: List[QuestionEngineReport] = Field(default_factory=list)

    # Section J (Gochara / Transit Intelligence)
    gochara_report: Optional[GocharaReport] = None
    
    # Section K (Developer Console)
    formula_verification: Dict[str, Any] = Field(default_factory=dict)
