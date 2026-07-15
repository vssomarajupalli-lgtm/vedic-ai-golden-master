export interface GlobalExecutiveSummaryDisplay {
    overall_score: number;
    overall_grade: string;
    overall_promise: string;
    current_mahadasha: string;
    current_antardasha: string;
    current_pratyantardasha: string;
    current_dasha_remaining: string;
    overall_lifetime_trend: string;
    strongest_life_area: string;
    weakest_life_area: string;
    best_planet: string;
    weak_planet: string;
    best_house: string;
    weak_house: string;
    upcoming_major_turning_point: string;
}

export interface LifetimeSnapshotDisplay {
    overall_promise: string;
    current_trend: string;
    current_opportunity: string;
    current_challenge: string;
    current_dasha: string;
    best_future_period: string;
    current_activation: string;
    current_grade: string;
}

export interface LifeAreaIntelligenceDisplay {
    domain_name: string;
    promise_percentage: number;
    grade: string;
    strengths: string[];
    weaknesses: string[];
    supporting_houses: string[];
    supporting_planets: string[];
    supporting_yogas: string[];
    current_dasha_influence: string;
    long_term_outlook: string;
    attention_factors: string[];
    interpretation: string;
    recommendations: string[];
}

export interface PlanetIntelligenceDisplay {
    planet_name: string;
    strength_score: number;
    functional_nature: string;
    dignity: string;
    lordship: string[];
    occupation: string;
    positive_contributions: string[];
    negative_contributions: string[];
    life_themes: string[];
    supporting_yogas: string[];
}

export interface HouseIntelligenceDisplay {
    house_name: string;
    score: number;
    grade: string;
    lord: string;
    occupants: string[];
}

export interface YogaIntelligenceDisplay {
    yoga_name: string;
    status: string;
    strength: number;
    meaning: string;
    supporting_area: string;
}

export interface CurrentDashaStatusDisplay {
    current_md: string;
    current_ad: string;
    current_pd: string;
    remaining_duration: string;
    current_activation: string;
    current_probability: number;
    current_grade: string;
    interpretation: string;
}

export interface DashaTimelineRowDisplay {
    age: number;
    start_date: string;
    end_date: string;
    md: string;
    ad: string;
    pd: string;
    md_strength: number;
    ad_strength: number;
    pd_strength: number;
    activation_percentage: number;
    probability_percentage: number;
    grade: string;
}

export interface LifetimeIntelligenceDashboard {
    snapshot: LifetimeSnapshotDisplay;
    life_areas: LifeAreaIntelligenceDisplay[];
    planets: PlanetIntelligenceDisplay[];
    houses: HouseIntelligenceDisplay[];
    yogas: YogaIntelligenceDisplay[];
    current_dasha_status: CurrentDashaStatusDisplay;
    timeline: DashaTimelineRowDisplay[];
}

export interface FinalReportSchema {
    report_version: string;
    generated_at: string;
    client_profile: Record<string, string>;
    executive_summary: GlobalExecutiveSummaryDisplay;
    lifetime_intelligence: LifetimeIntelligenceDashboard;
    question_responses: any[];
    formula_verification: Record<string, any>;
    engine_outputs: Record<string, any>;
    master_probability: {
        breakdown: Record<string, any>;
        lifetime_projection: any[];
    };
}


export interface ChartProcessResponse {
    status: string;
    final_score: number;
    probability_grade: string;
    breakdown: Record<string, any>;
    yogas: any[];
}

export interface QuestionResponse {
    question_id: string;
    answer_text: string;
    referenced_yogas: string[];
}

export interface StructuredQuestionResponse {
    question_id: string;
    results: any[];
}