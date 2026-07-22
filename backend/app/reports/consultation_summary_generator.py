import os
from typing import Dict, Any

class ConsultationSummaryGenerator:
    """
    Version 1.1 Enhancement: Astrologer's Prediction Summary Engine (APSE)
    A strict presentation layer that converts deterministic engine outputs
    into a concise one-page HTML summary. Performs ZERO calculations.
    """
    
    def __init__(self):
        pass

    def generate_html(self, output: Dict[str, Any], output_path: str = "outputs/consultation_summary.html") -> str:
        """
        Parses the deterministic output dictionary and generates a clean HTML summary report.
        """
        metadata = output.get("metadata", {})
        engines = output.get("engine_outputs", {})
        master = output.get("master_probability", {})
        
        # 1. Overall Snapshot
        natal_promise = engines.get("natal_promise", {})
        overall_natal = "Average" # Fallback if not summarized by engine, though we just display it
        # Actually, let's just grab Master Probability
        m_score = master.get("final_score", 0)
        m_grade = master.get("grade", "UNKNOWN")
        m_confidence = master.get("confidence", "MODERATE")
        
        dasha_engine_out = engines.get("dashas", {})
        active_dashas = []
        for p, d in dasha_engine_out.items():
            if not isinstance(d, dict):
                continue
            flags = d.get("confidence_flags", [])
            if "active_mahadasha" in flags:
                active_dashas.append(f"{p.capitalize()} (MD)")
            elif "active_antardasha" in flags:
                active_dashas.append(f"{p.capitalize()} (AD)")
            elif "active_pratyantardasha" in flags:
                active_dashas.append(f"{p.capitalize()} (PD)")
        current_dasha_str = " / ".join(active_dashas) if active_dashas else "Unknown"

        transit_engine_out = engines.get("transit", {})
        
        # 2 & 3. Planets
        planet_strengths = engines.get("planets", {})
        # Sort planets by final_score
        sorted_planets = sorted(planet_strengths.items(), key=lambda x: x[1].get("final_score", 0), reverse=True)
        top_3_planets = sorted_planets[:3]
        bottom_3_planets = sorted_planets[-3:] if len(sorted_planets) >= 3 else []
        
        # 4 & 5. Houses
        house_strengths = engines.get("houses", {})
        sorted_houses = sorted(house_strengths.items(), key=lambda x: x[1].get("final_score", 0), reverse=True)
        top_3_houses = sorted_houses[:3]
        bottom_3_houses = sorted_houses[-3:] if len(sorted_houses) >= 3 else []
        
        # 7. Key Consultation Areas (Questions)
        questions = engines.get("question_engine", [])
        # Only select high confidence or decent questions
        selected_questions = [q for q in questions if q.get("confidence") in ["High", "Very High", "Moderate", "good", "high"]]
        if not selected_questions:
            # Fallback to all if none match the exact string
            selected_questions = questions

        # 8. Yogas
        yogas = engines.get("yogas", {})
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Consultation Summary - {metadata.get('name', 'Client')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ border-bottom: 2px solid #2c3e50; padding-bottom: 10px; color: #2c3e50; }}
        h2 {{ color: #2980b9; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
        .snapshot-box {{ background: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .grid {{ display: flex; gap: 20px; }}
        .col {{ flex: 1; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .question-box {{ border-left: 4px solid #2980b9; padding-left: 15px; margin-bottom: 15px; background: #fdfdfd; padding-top: 5px; padding-bottom: 5px; }}
        .notes-section {{ height: 200px; border: 1px dashed #999; margin-top: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Astrologer's Consultation Summary</h1>
    <p><strong>Native:</strong> {metadata.get('name', 'Unknown')} | <strong>Lagna:</strong> {metadata.get('ascendant_sign', '?').capitalize()}</p>
    
    <h2>1. Overall Snapshot</h2>
    <div class="snapshot-box">
        <p><strong>Master Probability:</strong> {m_score}/100 ({m_grade})</p>
        <p><strong>Overall Confidence:</strong> {m_confidence}</p>
        <p><strong>Current Dasha:</strong> {current_dasha_str}</p>
    </div>

    <div class="grid">
        <div class="col">
            <h2>2. Strongest Planets</h2>
            <ul>
                {"".join([f"<li><strong>{p.capitalize()}</strong>: {d.get('final_score', 0)}/100</li>" for p, d in top_3_planets])}
            </ul>
        </div>
        <div class="col">
            <h2>3. Weakest Planets</h2>
            <ul>
                {"".join([f"<li><strong>{p.capitalize()}</strong>: {d.get('final_score', 0)}/100</li>" for p, d in reversed(bottom_3_planets)])}
            </ul>
        </div>
    </div>

    <div class="grid">
        <div class="col">
            <h2>4. Strongest Bhavas</h2>
            <ul>
                {"".join([f"<li><strong>{h.capitalize()}</strong>: {d.get('final_score', 0)}/100</li>" for h, d in top_3_houses])}
            </ul>
        </div>
        <div class="col">
            <h2>5. Weakest Bhavas</h2>
            <ul>
                {"".join([f"<li><strong>{h.capitalize()}</strong>: {d.get('final_score', 0)}/100</li>" for h, d in reversed(bottom_3_houses)])}
            </ul>
        </div>
    </div>

    <h2>6. Current Timing (Temporal Layer)</h2>
    <div class="snapshot-box">
        <p><strong>Dasha Sequence:</strong> {current_dasha_str}</p>
        <p><strong>Major Transit Influences:</strong> See detailed engineering report for full transit bindu activations.</p>
    </div>

    <h2>7. Key Consultation Areas</h2>
"""
        for q in selected_questions:
            domain = q.get("domain", "General").capitalize()
            prob_dict = q.get("probability", {})
            prob = prob_dict.get("score", 0)
            prob_grade = prob_dict.get("grade", "?")
            conf = q.get("confidence", "MODERATE").upper()
            q_text = q.get("question", domain)
            engines_used = q.get("engines_used", ["MasterProbabilityEngine", "NatalPromiseEngine", "DashaEngine"])
            html += f"""    <div class="question-box">
        <h4>{q_text}</h4>
        <p><strong>Probability:</strong> {prob}/100 ({prob_grade}) | <strong>Confidence:</strong> {conf}</p>
        <p><em>Supporting Engines:</em> {", ".join(engines_used)}</p>
    </div>
"""

        html += f"""
    <h2>8. Important Yogas</h2>
    <div class="snapshot-box">
"""
        if yogas:
            html += "<ul>"
            for y_category, y_list in yogas.items():
                if isinstance(y_list, list) and y_list:
                    html += f"<li><strong>{y_category.replace('_', ' ').capitalize()}</strong>: {', '.join(y_list)}</li>"
            html += "</ul>"
        else:
            html += "<p>No major yogas highlighted by the engine.</p>"

        html += """    </div>

    <h2>9. Astrologer's Notes</h2>
    <p><em>(Observations, Recommendations, Remedies)</em></p>
    <div class="notes-section"></div>

</body>
</html>
"""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
            
        return html
