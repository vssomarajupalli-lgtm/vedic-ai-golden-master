from app.formulas.schema import FormulaSchema

# Seed formulas implemented strictly as data structs (no logic)
# Based on PHASE 12B FORMULA_REPOSITORY_DATA_MODEL_v1.md

SEED_FORMULAS = [
    # ---------------------------------------------------------
    # MARRIAGE FAMILY
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="MAR_TIMING_BASE",
        formula_name="Marriage Timing Base",
        formula_category="Timing Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["7th_house", "7th_lord", "venus", "lagna_lord"],
        required_dasha_layers=["mahadasha", "antardasha"],
        required_confidence_layers=["dasha_lord_aspect_7th", "dasha_lord_is_venus"],
        answer_template_key="timing_assessment_v1"
    ),
    FormulaSchema(
        formula_key="MAR_TIMING_NORMAL",
        formula_name="Standard Marriage Timing",
        formula_category="Timing Assessment",
        parent_formula_key="MAR_TIMING_BASE",
        required_confidence_layers=["absence_of_saturn_delay"],
        answer_template_key="timing_assessment_v1"
    ),
    FormulaSchema(
                formula_key="MAR_TIMING_DELAY",
                formula_name="Delayed Marriage Timing",
                formula_category="Timing Assessment",
                parent_formula_key="MAR_TIMING_BASE",
                required_engines=["TransitEngine"],
                required_signals=["saturn"],
                required_confidence_layers=["saturn_aspect_7th"],
                future_gochara_required=True,
                answer_template_key="timing_assessment_v1"
            ),

    # ---------------------------------------------------------
    # CAREER FAMILY
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="CAR_GROWTH_BASE",
        formula_name="Career Growth Base",
        formula_category="Timing Assessment",
        required_engines=["NatalPromiseEngine", "AshtakavargaEngine", "DashaEngine"],
        required_signals=["10th_house", "10th_lord", "11th_house"],
        required_vargas=["D1", "D10"],
        required_confidence_layers=["10th_lord_d10_strength", "positive_dasha"],
        answer_template_key="timing_assessment_v1"
    ),
    FormulaSchema(
        formula_key="CAR_PROMOTION_TIMING",
        formula_name="Promotion Timing",
        formula_category="Timing Assessment",
        parent_formula_key="CAR_GROWTH_BASE",
        required_confidence_layers=["10th_house_bindus_gt_28"],
        answer_template_key="timing_assessment_v1"
    ),
    FormulaSchema(
        formula_key="CAR_CHANGE_TIMING",
        formula_name="Job Change Timing",
        formula_category="Timing Assessment",
        parent_formula_key="CAR_GROWTH_BASE",
        required_engines=["TransitEngine"],
        required_signals=["5th_house", "9th_house"],
        required_confidence_layers=["dasha_lords_connect_5th_9th"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # WEALTH FAMILY
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="WEA_SUDDEN_BASE",
        formula_name="Sudden Wealth Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["8th_house", "11th_house", "rahu", "2nd_house"],
        required_vargas=["D1"],
        required_confidence_layers=["8th_lord_connect_11th", "dasha_activates_yoga"],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="WEA_SUDDEN_GAIN",
        formula_name="Sudden Financial Gains",
        formula_category="Multi-factor Assessment",
        parent_formula_key="WEA_SUDDEN_BASE",
        required_confidence_layers=["rahu_in_8th_11th", "absence_malefic_aspect_2nd"],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="WEA_SUDDEN_LOSS",
        formula_name="Sudden Financial Loss",
        formula_category="Multi-factor Assessment",
        parent_formula_key="WEA_SUDDEN_BASE",
        required_signals=["12th_house"],
        required_confidence_layers=["rahu_afflicts_2nd_lord", "12th_lord_active"],
        answer_template_key="multifactor_assessment_v1"
    ),

    # ---------------------------------------------------------
    # HEALTH FAMILY (Domain 6)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="HLT_LONGEVITY_BASE",
        formula_name="Longevity Assessment Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["lagna", "8th_house", "8th_lord", "saturn"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="HLT_LONGEVITY_ASSESSMENT",
        formula_name="Longevity Assessment",
        formula_category="Multi-factor Assessment",
        parent_formula_key="HLT_LONGEVITY_BASE",
        required_confidence_layers=["8th_house_strength", "saturn_dignity"],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="HLT_VITALITY_BASE",
        formula_name="Health and Vitality Base",
        formula_category="Strength Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["lagna", "lagna_lord", "sun", "moon", "6th_house", "6th_lord", "8th_house", "12th_house"],
        required_confidence_layers=[],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="HLT_GENERAL_VITALITY",
        formula_name="General Health and Vitality",
        formula_category="Strength Assessment",
        parent_formula_key="HLT_VITALITY_BASE",
        required_confidence_layers=["lagna_strength", "sun_dignity", "moon_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="HLT_ILLNESS_RISK",
        formula_name="Illness Risk Assessment",
        formula_category="Risk Assessment",
        parent_formula_key="HLT_VITALITY_BASE",
        required_confidence_layers=["6th_lord_activation", "8th_lord_activation", "12th_house_activation", "malefic_aspect_lagna"],
        answer_template_key="risk_assessment_v1"
    ),
    FormulaSchema(
        formula_key="HLT_RECOVERY_TIMING",
        formula_name="Recovery Timing",
        formula_category="Timing Assessment",
        parent_formula_key="HLT_VITALITY_BASE",
        required_confidence_layers=["positive_dasha"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # PROPERTY FAMILY (Domain 4)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="AST_VEHICLE_BASE",
        formula_name="Vehicle Asset Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine"],
        required_signals=["4th_house", "4th_lord", "venus", "jupiter", "11th_house"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="AST_PROPERTY_BASE",
        formula_name="Property Asset Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["4th_house", "4th_lord", "mars", "jupiter", "2nd_house", "11th_house"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="AST_PROP_PROMISE",
        formula_name="Property Promise",
        formula_category="Strength Assessment",
        parent_formula_key="AST_PROPERTY_BASE",
        required_confidence_layers=["4th_house_strength", "mars_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="AST_PROP_TIMING",
        formula_name="Property Purchase Timing",
        formula_category="Timing Assessment",
        parent_formula_key="AST_PROPERTY_BASE",
        required_confidence_layers=["dasha_activates_4th", "2nd_11th_lord_activation"],
        answer_template_key="timing_assessment_v1"
    ),
    FormulaSchema(
        formula_key="AST_PROP_LOSS_RISK",
        formula_name="Property Loss Risk",
        formula_category="Risk Assessment",
        parent_formula_key="AST_PROPERTY_BASE",
        required_confidence_layers=["4th_lord_in_8th_or_12th", "malefic_aspect_4th"],
        answer_template_key="risk_assessment_v1"
    ),

    # ---------------------------------------------------------
    # EDUCATION FAMILY (Domain 4, 5, 9)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="EDU_ACADEMIC_BASE",
        formula_name="Education Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine", "YogaEngine"],
        required_signals=["4th_house", "5th_house", "9th_house", "12th_house", "mercury", "jupiter", "moon", "rahu"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="EDU_ACADEMIC_SUCCESS",
        formula_name="Academic Success",
        formula_category="Strength Assessment",
        parent_formula_key="EDU_ACADEMIC_BASE",
        required_confidence_layers=["4th_house_strength", "5th_house_strength", "mercury_dignity", "moon_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="EDU_HIGHER_ACADEMICS",
        formula_name="Higher Academics",
        formula_category="Strength Assessment",
        parent_formula_key="EDU_ACADEMIC_BASE",
        required_confidence_layers=["9th_house_strength", "jupiter_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="EDU_FOREIGN_STUDY",
        formula_name="Foreign Study",
        formula_category="Strength Assessment",
        parent_formula_key="EDU_ACADEMIC_BASE",
        required_confidence_layers=["12th_house_activation", "9th_house_activation", "rahu_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="EDU_EXAM_SUCCESS_TIMING",
        formula_name="Competitive Exam Timing",
        formula_category="Timing Assessment",
        parent_formula_key="EDU_ACADEMIC_BASE",
        required_signals=["6th_house"],
        required_confidence_layers=["dasha_activates_5th_6th"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # PROGENY FAMILY (Domain 5, 9)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="FAM_PROGENY_BASE",
        formula_name="Progeny and Children Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["5th_house", "5th_lord", "9th_house", "jupiter"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="FAM_CHILD_PROMISE",
        formula_name="Child Promise",
        formula_category="Strength Assessment",
        parent_formula_key="FAM_PROGENY_BASE",
        required_confidence_layers=["5th_house_strength", "jupiter_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="FAM_CHILD_TIMING",
        formula_name="Childbirth Timing",
        formula_category="Timing Assessment",
        parent_formula_key="FAM_PROGENY_BASE",
        required_confidence_layers=["dasha_activates_5th_9th"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # LITIGATION FAMILY (Domain 6)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="LIT_CONFLICT_BASE",
        formula_name="Litigation and Conflict Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["1st_house", "1st_lord", "6th_house", "6th_lord", "mars", "saturn"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="LIT_LEGAL_VICTORY",
        formula_name="Legal Victory Assessment",
        formula_category="Strength Assessment",
        parent_formula_key="LIT_CONFLICT_BASE",
        required_confidence_layers=["1st_lord_stronger_than_6th_lord", "mars_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="LIT_DEBT_RISK",
        formula_name="Debt Risk Assessment",
        formula_category="Risk Assessment",
        parent_formula_key="LIT_CONFLICT_BASE",
        required_signals=["2nd_house", "11th_house"],
        required_confidence_layers=["6th_lord_in_2nd_or_11th", "saturn_afflicts_lagna"],
        answer_template_key="risk_assessment_v1"
    ),
    FormulaSchema(
        formula_key="LIT_CONFLICT_TIMING",
        formula_name="Conflict Timing",
        formula_category="Timing Assessment",
        parent_formula_key="LIT_CONFLICT_BASE",
        required_confidence_layers=["dasha_activates_6th"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # TRAVEL FAMILY (Domain 3, 9, 12)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="TRV_RELOCATION_BASE",
        formula_name="Travel and Relocation Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["3rd_house", "4th_house", "9th_house", "12th_house", "moon", "rahu"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="TRV_SHORT_TRIP",
        formula_name="Short Trip Assessment",
        formula_category="Strength Assessment",
        parent_formula_key="TRV_RELOCATION_BASE",
        required_confidence_layers=["3rd_house_strength", "moon_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="TRV_FOREIGN_SETTLEMENT",
        formula_name="Foreign Settlement Assessment",
        formula_category="Strength Assessment",
        parent_formula_key="TRV_RELOCATION_BASE",
        required_confidence_layers=["12th_house_strength", "rahu_dignity", "4th_house_afflicted"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="TRV_TIMING",
        formula_name="Travel Timing",
        formula_category="Timing Assessment",
        parent_formula_key="TRV_RELOCATION_BASE",
        required_confidence_layers=["dasha_activates_3rd_9th_12th"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # SPIRITUALITY FAMILY (Domain 9, 12, 5)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="SPR_MOKSHA_BASE",
        formula_name="Spirituality Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["5th_house", "9th_house", "12th_house", "jupiter", "ketu"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="SPR_SPIRITUAL_PROGRESS",
        formula_name="Spiritual Progress",
        formula_category="Strength Assessment",
        parent_formula_key="SPR_MOKSHA_BASE",
        required_confidence_layers=["9th_house_strength", "12th_house_strength", "ketu_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="SPR_MANTRA_SIDDHI",
        formula_name="Mantra Siddhi",
        formula_category="Strength Assessment",
        parent_formula_key="SPR_MOKSHA_BASE",
        required_confidence_layers=["5th_house_strength", "jupiter_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="SPR_ISOLATION_TIMING",
        formula_name="Isolation/Pilgrimage Timing",
        formula_category="Timing Assessment",
        parent_formula_key="SPR_MOKSHA_BASE",
        required_confidence_layers=["dasha_activates_9th_12th"],
        answer_template_key="timing_assessment_v1"
    ),

    # ---------------------------------------------------------
    # COMPATIBILITY FAMILY (Domain 7)
    # ---------------------------------------------------------
    FormulaSchema(
        formula_key="REL_DYNAMICS_BASE",
        formula_name="Relationship Dynamics Base",
        formula_category="Multi-factor Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["7th_house", "7th_lord", "2nd_house", "venus", "moon"],
        required_confidence_layers=[],
        answer_template_key="multifactor_assessment_v1"
    ),
    FormulaSchema(
        formula_key="REL_MARITAL_HARMONY",
        formula_name="Marital Harmony",
        formula_category="Strength Assessment",
        parent_formula_key="REL_DYNAMICS_BASE",
        required_confidence_layers=["7th_house_strength", "2nd_house_strength", "venus_dignity", "moon_dignity"],
        answer_template_key="strength_assessment_v1"
    ),
    FormulaSchema(
        formula_key="REL_DIVORCE_RISK",
        formula_name="Divorce Risk Assessment",
        formula_category="Risk Assessment",
        parent_formula_key="REL_DYNAMICS_BASE",
        required_confidence_layers=["7th_lord_in_6th_8th_12th", "malefic_aspect_7th"],
        answer_template_key="risk_assessment_v1"
    )
]

def get_seed_registry():
    return SEED_FORMULAS
