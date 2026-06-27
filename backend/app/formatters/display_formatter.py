from typing import Dict, Any, List
from datetime import datetime
from app.schemas.question import (
    StructuredQuestionResult,
    ExecutiveSummaryDisplay,
    CurrentDashaStatusDisplay as QCurrentDashaStatusDisplay,
    FutureOpportunityWindowDisplay,
    DetailedAnalysisDisplay,
    SupportingFactorDisplay,
    AttentionFactorDisplay,
    LifetimeSummaryDisplay,
    TechnicalLifetimeRecord,
    FormulaVerificationDisplay
)
from app.reports.schemas import (
    GlobalExecutiveSummaryDisplay,
    LifetimeSnapshotDisplay,
    LifeAreaIntelligenceDisplay,
    PlanetIntelligenceDisplay,
    HouseIntelligenceDisplay,
    YogaIntelligenceDisplay,
    CurrentDashaStatusDisplay,
    DashaTimelineRowDisplay,
    LifetimeIntelligenceDashboard
)

class DisplayFormatter:
    """
    Transforms internal mathematical outputs and Boolean gate results into 
    the highly structured Questionnaire Display format (Phase 16E).
    Strictly Presentation Layer. Zero Architectural Modifications.
    """
    
    @staticmethod
    def _map_display_grade(internal_grade: str) -> str:
        mapping = {
            "PRESENT": "Very Weak",
            "WEAK": "Weak",
            "MODERATE": "Moderate",
            "STRONG": "Good",
            "EXCELLENT": "Excellent"
        }
        return mapping.get(internal_grade.upper(), internal_grade.capitalize())

    @staticmethod
    def format_percentage(score: float, grade_str: str = None) -> str:
        """
        Enforces Phase 16D Rule: 84% (Excellent).
        Never returns just 'Excellent' or just '84%'.
        """
        try:
            val = round(float(score))
        except (ValueError, TypeError):
            val = 50
            
        if not grade_str:
            if val >= 80:
                grade = "Excellent"
            elif val >= 60:
                grade = "Good"
            elif val >= 40:
                grade = "Moderate"
            else:
                grade = "Weak"
        else:
            grade = DisplayFormatter._map_display_grade(grade_str)
            
        return f"{val}% ({grade})"

    @staticmethod
    def format_date(date_str: str) -> str:
        if not date_str or date_str == "Unknown":
            return "Unknown"
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d %b %Y").lstrip("0")
        except ValueError:
            return date_str
            
    @staticmethod
    def calculate_age(dob: str, target_date: str) -> str:
        if not dob or not target_date or dob == "Unknown" or target_date == "Unknown":
            return 0
        try:
            dob_dt = datetime.strptime(dob, "%Y-%m-%d")
            target_dt = datetime.strptime(target_date, "%Y-%m-%d")
            age_years = (target_dt - dob_dt).days // 365
            return int(age_years)
        except ValueError:
            return 0

    @staticmethod
    def _calculate_remaining_dasha(ends_on_raw: str) -> str:
        remaining = "Unknown"
        if ends_on_raw != "Unknown":
            try:
                end_dt = datetime.strptime(ends_on_raw, "%Y-%m-%d")
                now_dt = datetime.now()
                days_left = (end_dt - now_dt).days
                if days_left > 30:
                    remaining = f"{days_left // 30} months"
                elif days_left > 0:
                    remaining = f"{days_left} days"
                else:
                    remaining = "Ended"
            except:
                pass
        return remaining

    @staticmethod
    def format_question_result(
        question_title: str,
        domain: str,
        natal_promise: Dict[str, Any],
        dasha_activation: Dict[str, Any],
        lifetime_projection: List[Dict[str, Any]],
        final_state: str,
        isolated_signals: Dict[str, Any],
        client_metadata: Dict[str, Any] = None
    ) -> StructuredQuestionResult:
        
        client_metadata = client_metadata or {}
        dob = client_metadata.get("dob", "Unknown")
        
        domain_promise = natal_promise.get(domain, {})
        p_score = domain_promise.get("score", 50)
        p_grade_internal = domain_promise.get("promise", "MODERATE")
        promise_display = DisplayFormatter.format_percentage(p_score, p_grade_internal)
        
        synthesis = dasha_activation.get("synthesis", {})
        current_md = synthesis.get("active_md", "unknown").capitalize()
        current_ad = synthesis.get("active_ad", "unknown").capitalize()
        current_pd = synthesis.get("active_pd", "unknown").capitalize()
        md_str = synthesis.get("md_strength", 50.0)
        ad_str = synthesis.get("ad_strength", 50.0)
        pd_str = synthesis.get("pd_strength", 50.0)
        
        act_score = round((md_str + ad_str + pd_str) / 3.0)
        current_activation_display = DisplayFormatter.format_percentage(act_score)
        
        current_prob_score = round((p_score * 0.6) + (act_score * 0.4))
        current_prob_display = DisplayFormatter.format_percentage(current_prob_score)
        
        ends_on_raw = synthesis.get("pd_end", "Unknown")
        ends_on = DisplayFormatter.format_date(ends_on_raw)
        remaining_duration = DisplayFormatter._calculate_remaining_dasha(ends_on_raw)

        current_dasha = QCurrentDashaStatusDisplay(
            current_md=current_md,
            current_ad=current_ad,
            current_pd=current_pd,
            current_activation_display=current_activation_display,
            current_probability_display=current_prob_display,
            remaining_duration=remaining_duration,
            ends_on=ends_on
        )
        
        future_windows = []
        
        if lifetime_projection:
            # Sort by final_probability_pct (descending)
            ranked_timeline = sorted(
                lifetime_projection, 
                key=lambda x: x.get("final_probability_pct", 0), 
                reverse=True
            )
            
            strong_count = mod_count = weak_count = highest_act = highest_prob = 0
            best_window = "Unknown"
            
            # First pass: gather lifetime summary statistics (on chronological or ranked, doesn't matter for aggregate)
            for item in lifetime_projection:
                t_act = int(item.get("activation_pct", 50))
                t_prob = int(item.get("final_probability_pct", 50))
                
                t_start_raw = item.get("start_date", "Unknown")
                t_end_raw = item.get("end_date", "Unknown")
                t_start = DisplayFormatter.format_date(t_start_raw)
                t_end = DisplayFormatter.format_date(t_end_raw)
                
                if t_act >= 70: strong_count += 1
                elif t_act >= 50: mod_count += 1
                else: weak_count += 1
                    
                if t_act > highest_act: highest_act = t_act
                if t_prob > highest_prob:
                    highest_prob = t_prob
                    best_window = f"{t_start} - {t_end}"
            
            # Second pass: extract top 5 future windows
            for rank, item in enumerate(ranked_timeline[:5], 1):
                t_md = item.get("md", "unknown").capitalize()
                t_ad = item.get("ad", "unknown").capitalize()
                t_pd = item.get("pd", "unknown").capitalize()
                
                t_prob = int(item.get("final_probability_pct", 50))
                t_prob_display = DisplayFormatter.format_percentage(t_prob)
                
                t_start_raw = item.get("start_date", "Unknown")
                t_end_raw = item.get("end_date", "Unknown")
                t_start = DisplayFormatter.format_date(t_start_raw)
                t_end = DisplayFormatter.format_date(t_end_raw)
                t_age = str(DisplayFormatter.calculate_age(dob, t_start_raw)) + " yrs"
                
                fw = FutureOpportunityWindowDisplay(
                    rank=rank,
                    start_date=t_start,
                    end_date=t_end,
                    age=t_age,
                    mahadasha=t_md,
                    antardasha=t_ad,
                    pratyantardasha=t_pd,
                    final_probability_display=t_prob_display,
                    astrological_driver=f"{t_md} MD, {t_ad} AD"
                )
                future_windows.append(fw)
        else:
            strong_count = mod_count = weak_count = highest_act = highest_prob = 0
            best_window = "Unknown"

        overall_direction = "Stable"
        if strong_count > weak_count * 2: overall_direction = "Improving"
        elif weak_count > strong_count * 2: overall_direction = "Challenging"
            
        lifetime_summary = LifetimeSummaryDisplay(
            strong_period_count=strong_count,
            moderate_period_count=mod_count,
            weak_period_count=weak_count,
            highest_activation_display=DisplayFormatter.format_percentage(highest_act),
            highest_probability_display=DisplayFormatter.format_percentage(highest_prob),
            best_lifetime_window=best_window,
            longest_strong_window=best_window,
            current_lifetime_rank="Average"
        )
        
        supporting_factors = []
        attention_factors = []
        main_strength = "Balanced Chart"
        main_weakness = "No major weaknesses"
        
        def format_signal_name(s: str) -> str:
            return " ".join(word.capitalize() for word in s.split('_'))

        sorted_signals = sorted(isolated_signals.items(), key=lambda x: x[1].get("final_score", 0), reverse=True)
        
        for idx, (sig_key, sig_data) in enumerate(sorted_signals):
            name = format_signal_name(sig_key)
            score = sig_data.get("final_score", 0)
            
            if score >= 50:
                if len(supporting_factors) == 0: main_strength = name
                supporting_factors.append(SupportingFactorDisplay(
                    title=name,
                    explanation=f"{name} is strong.",
                    impact="High Positive" if score >= 80 else "Moderate Positive"
                ))
            else:
                if len(attention_factors) == 0: main_weakness = name
                attention_factors.append(AttentionFactorDisplay(
                    reason=f"{name} lacks necessary strength.",
                    impact="May cause delays or require extra effort.",
                    severity="High" if score < 30 else "Medium",
                    recommendation="Patience is required."
                ))

        best_fw_disp = future_windows[0].final_probability_display if future_windows else "Unknown"
        best_fw_win = f"{future_windows[0].start_date} - {future_windows[0].end_date}" if future_windows else "Unknown"
        
        exec_summary = ExecutiveSummaryDisplay(
            promise_display=promise_display,
            current_support_display=current_activation_display,
            best_future_opportunity_display=best_fw_disp,
            best_future_window=best_fw_win,
            main_strength=main_strength,
            main_weakness=main_weakness,
            recommendation=f"Leverage your {main_strength}. Prepare for periods impacted by {main_weakness}.",
            current_period_remaining=remaining_duration,
            overall_lifetime_direction=overall_direction
        )

        detailed_analysis = DetailedAnalysisDisplay(
            natural_language_explanation=f"Your chart indicates a {promise_display.lower()} foundation for {domain}."
        )

        formula_verification = FormulaVerificationDisplay(
            data_lineage=isolated_signals
        )

        return StructuredQuestionResult(
            question_title=question_title,
            domain=domain.replace("_", " ").title(),
            executive_summary=exec_summary,
            current_dasha_status=current_dasha,
            future_opportunities=future_windows,
            detailed_analysis=detailed_analysis,
            supporting_factors=supporting_factors,
            attention_factors=attention_factors,
            lifetime_summary=lifetime_summary,
            formula_verification=formula_verification
        )

    @staticmethod
    def format_executive_summary(pipeline_data: Dict[str, Any]) -> GlobalExecutiveSummaryDisplay:
        engine_outputs = pipeline_data.get("engine_outputs", {})
        promise = engine_outputs.get("natal_promise", {})
        dashas = engine_outputs.get("dashas", {}).get("timeline", [])
        synthesis = engine_outputs.get("dashas", {}).get("synthesis", {})
        
        total_score = 0
        count = 0
        for k, v in promise.items():
            if isinstance(v, dict) and 'score' in v:
                total_score += v.get("score", 50)
                count += 1
                
        overall_score = round(total_score / count) if count > 0 else 50
        overall_grade = DisplayFormatter.format_percentage(overall_score)
        
        sorted_areas = sorted([(k, v.get("score", 50)) for k, v in promise.items() if isinstance(v, dict)], key=lambda x: x[1], reverse=True)
        strongest = [k.replace("_", " ").title() for k, v in sorted_areas[:1]]
        weakest = [k.replace("_", " ").title() for k, v in sorted_areas[-1:]]
        
        current_md = synthesis.get("active_md", "Unknown").capitalize()
        current_ad = synthesis.get("active_ad", "Unknown").capitalize()
        current_pd = synthesis.get("active_pd", "Unknown").capitalize()
        
        ends_on_raw = synthesis.get("pd_end", "Unknown")
        remaining = DisplayFormatter._calculate_remaining_dasha(ends_on_raw)
        
        trend = "Stable"
        if overall_score >= 70: trend = "Improving"
        elif overall_score < 40: trend = "Challenging"

        planets = engine_outputs.get("planets", {})
        sorted_planets = sorted([(k, v.get("score", 50)) for k, v in planets.items() if k not in ["ascendant", "lagna"]], key=lambda x: x[1], reverse=True)
        best_planet = sorted_planets[0][0].capitalize() if sorted_planets else "Unknown"
        weak_planet = sorted_planets[-1][0].capitalize() if sorted_planets else "Unknown"

        houses = engine_outputs.get("houses", {})
        sorted_houses = sorted([(k, v.get("score", 50)) for k, v in houses.items() if k.endswith("_house")], key=lambda x: x[1], reverse=True)
        best_house = sorted_houses[0][0].replace("_house", "").capitalize() if sorted_houses else "Unknown"
        weak_house = sorted_houses[-1][0].replace("_house", "").capitalize() if sorted_houses else "Unknown"

        return GlobalExecutiveSummaryDisplay(
            overall_score=overall_score,
            overall_grade=overall_grade,
            overall_promise=overall_grade,
            current_mahadasha=current_md,
            current_antardasha=current_ad,
            current_pratyantardasha=current_pd,
            current_dasha_remaining=remaining,
            overall_lifetime_trend=trend,
            strongest_life_area=strongest[0] if strongest else "None",
            weakest_life_area=weakest[0] if weakest else "None",
            best_planet=best_planet,
            weak_planet=weak_planet,
            best_house=best_house,
            weak_house=weak_house,
            upcoming_major_turning_point="End of " + current_md
        )

    @staticmethod
    def format_lifetime_dashboard(pipeline_data: Dict[str, Any], client_metadata: Dict[str, Any] = None) -> LifetimeIntelligenceDashboard:
        client_metadata = client_metadata or {}
        dob = client_metadata.get("dob", "Unknown")
        
        engine_outputs = pipeline_data.get("engine_outputs", {})
        planets = engine_outputs.get("planets", {})
        houses = engine_outputs.get("houses", {})
        promise = engine_outputs.get("natal_promise", {})
        synthesis = engine_outputs.get("dashas", {}).get("synthesis", {})
        timeline_raw = pipeline_data.get("master_probability", {}).get("lifetime_projection", [])
        yogas = engine_outputs.get("yogas", {}).get("active_yogas", [])

        # House Intelligence
        house_domain_map = {
            1: "Personality", 2: "Wealth & Family", 3: "Communication", 4: "Mother & Property",
            5: "Education & Children", 6: "Health & Service", 7: "Marriage & Partnership",
            8: "Transformation", 9: "Fortune & Religion", 10: "Career", 11: "Income", 12: "Spirituality"
        }
        
        house_list = []
        for h_key, h_data in houses.items():
            if not h_key.endswith("_house"): continue
            try:
                num = int(h_key.split("_")[0].replace("th","").replace("st","").replace("nd","").replace("rd",""))
            except:
                num = 0
            
            h_score = h_data.get("score", 50)
            h_grade = DisplayFormatter._map_display_grade(h_data.get("strength_category", "MODERATE"))
            
            domain_name = house_domain_map.get(num, f"House {num}")
            
            house_list.append(HouseIntelligenceDisplay(
                house_name=domain_name,
                score=h_score,
                grade=DisplayFormatter.format_percentage(h_score, h_grade),
                lord=h_data.get("lord", "unknown").capitalize(),
                occupants=h_data.get("occupants", [])
            ))
        house_list.sort(key=lambda x: list(house_domain_map.values()).index(x.house_name) if x.house_name in house_domain_map.values() else 99)

        # Planet Intelligence
        planet_list = []
        for p_key, p_data in planets.items():
            if p_key in ["ascendant", "lagna"]: continue
            p_score = p_data.get("score", 50)
            p_grade = DisplayFormatter._map_display_grade(p_data.get("strength_category", "MODERATE"))
            
            planet_list.append(PlanetIntelligenceDisplay(
                planet_name=p_key.capitalize(),
                strength_score=p_score,
                functional_nature=pipeline_data.get("functional_nature", {}).get(p_key, "Neutral").capitalize(),
                dignity=p_data.get("dignity", "neutral").capitalize(),
                lordship=[],
                occupation="Unknown",
                positive_contributions=[f"Strong influence when dignified"] if p_score >= 60 else [],
                negative_contributions=[f"May cause delays if afflicted"] if p_score < 40 else [],
                life_themes=[f"Matters related to {p_key.capitalize()}"],
                supporting_yogas=[]
            ))

        # Life Areas
        life_areas = []
        for d_key, d_data in promise.items():
            if isinstance(d_data, dict) and 'score' in d_data:
                d_score = d_data.get("score", 50)
                d_grade = DisplayFormatter._map_display_grade(d_data.get("promise", "MODERATE"))
                life_areas.append(LifeAreaIntelligenceDisplay(
                    domain_name=d_key.replace("_", " ").title(),
                    promise_percentage=d_score,
                    grade=DisplayFormatter.format_percentage(d_score, d_grade),
                    strengths=[],
                    weaknesses=[],
                    supporting_houses=[],
                    supporting_planets=[],
                    supporting_yogas=[],
                    current_dasha_influence="Positive" if d_score >= 60 else "Neutral",
                    long_term_outlook="Promising" if d_score >= 70 else "Stable" if d_score >= 40 else "Challenging",
                    attention_factors=[f"Requires attention due to lower strength"] if d_score < 50 else [],
                    interpretation=f"The domain of {d_key.replace('_', ' ').title()} indicates {d_grade.lower()} promise based on planetary and house strengths.",
                    recommendations=[f"Focus on strengthening the factors related to {d_key.replace('_', ' ').title()}."] if d_score < 50 else [f"Leverage your natural strengths in {d_key.replace('_', ' ').title()}."]
                ))

        # Yogas
        yoga_list = []
        for y in yogas:
            y_name = y.get("yoga_name", "Unknown Yoga")
            y_str = y.get("strength", 50)
            yoga_list.append(YogaIntelligenceDisplay(
                yoga_name=y_name,
                status="Present",
                strength=int(y_str),
                meaning=y.get("meaning", f"Enhances {y_name}"),
                supporting_area=y.get("supporting_area", "General")
            ))

        # Current Dasha Status
        current_md = synthesis.get("active_md", "Unknown").capitalize()
        current_ad = synthesis.get("active_ad", "Unknown").capitalize()
        current_pd = synthesis.get("active_pd", "Unknown").capitalize()
        ends_on_raw = synthesis.get("pd_end", "Unknown")
        remaining = DisplayFormatter._calculate_remaining_dasha(ends_on_raw)
        
        md_str = synthesis.get("md_strength", 50.0)
        ad_str = synthesis.get("ad_strength", 50.0)
        pd_str = synthesis.get("pd_strength", 50.0)
        act_score = round((md_str + ad_str + pd_str) / 3.0)
        act_grade = DisplayFormatter._map_display_grade("STRONG" if act_score >= 70 else "MODERATE")
        
        dasha_status = CurrentDashaStatusDisplay(
            current_md=current_md,
            current_ad=current_ad,
            current_pd=current_pd,
            remaining_duration=remaining,
            current_activation=DisplayFormatter.format_percentage(act_score),
            current_probability=int(act_score),
            current_grade=act_grade,
            interpretation=f"Current period focuses on themes related to {current_md} and {current_ad}."
        )

        # Timeline
        timeline_rows = []
        for item in timeline_raw:
            t_md = item.get("md", "unknown").capitalize()
            t_ad = item.get("ad", "unknown").capitalize()
            t_pd = item.get("pd", "unknown").capitalize()
            t_start_raw = item.get("start_date", "Unknown")
            t_end_raw = item.get("end_date", "Unknown")
            
            t_md_str = int(item.get("md_planet_strength", 50))
            t_ad_str = int(item.get("ad_planet_strength", 50))
            t_pd_str = int(item.get("pd_planet_strength", 50))
            
            t_act = int(item.get("activation_pct", 50))
            t_prob = int(item.get("final_probability_pct", 50))
            t_grade = item.get("grade", "UNKNOWN")
            
            timeline_rows.append(DashaTimelineRowDisplay(
                age=DisplayFormatter.calculate_age(dob, t_start_raw),
                start_date=DisplayFormatter.format_date(t_start_raw),
                end_date=DisplayFormatter.format_date(t_end_raw),
                md=t_md,
                ad=t_ad,
                pd=t_pd,
                md_strength=t_md_str,
                ad_strength=t_ad_str,
                pd_strength=t_pd_str,
                activation_percentage=t_act,
                probability_percentage=t_prob,
                grade=DisplayFormatter._map_display_grade(t_grade)
            ))
            
        timeline_rows.sort(key=lambda x: datetime.strptime(x.start_date, "%d %b %Y") if x.start_date != "Unknown" else datetime.min)

        # Dynamic Snapshot Logic
        total_score = 0
        count = 0
        for k, v in promise.items():
            if isinstance(v, dict) and 'score' in v:
                total_score += v.get("score", 50)
                count += 1
        overall_score = round(total_score / count) if count > 0 else 50
        overall_promise_disp = DisplayFormatter.format_percentage(overall_score)
        
        current_trend = "Stable"
        if overall_score >= 70: current_trend = "Improving"
        elif overall_score < 40: current_trend = "Challenging"
        
        sorted_areas = sorted([(k, v.get("score", 50)) for k, v in promise.items() if isinstance(v, dict)], key=lambda x: x[1], reverse=True)
        current_opp = sorted_areas[0][0].replace("_", " ").title() if sorted_areas else "None"
        current_chal = sorted_areas[-1][0].replace("_", " ").title() if sorted_areas else "None"
        
        best_future_period = "Unknown"
        highest_act = 0
        for item in timeline_raw:
            t_act = int(item.get("activation_pct", 50))
            if t_act > highest_act:
                highest_act = t_act
                best_future_period = item.get("start_date", "Unknown")
        
        # Snapshot
        snapshot = LifetimeSnapshotDisplay(
            overall_promise=overall_promise_disp,
            current_trend=current_trend,
            current_opportunity=current_opp,
            current_challenge=current_chal,
            current_dasha=f"{current_md}-{current_ad}",
            best_future_period=DisplayFormatter.format_date(best_future_period),
            current_activation=DisplayFormatter.format_percentage(act_score),
            current_grade=act_grade
        )

        return LifetimeIntelligenceDashboard(
            snapshot=snapshot,
            life_areas=life_areas,
            planets=planet_list,
            houses=house_list,
            yogas=yoga_list,
            current_dasha_status=dasha_status,
            timeline=timeline_rows
        )
