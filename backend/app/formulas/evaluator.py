from typing import Dict, Any, List
from app.formulas.schema import FormulaSchema, FormulaEvaluationResult

class FormulaEvaluator:

    @staticmethod
    def check_engine_degradation(formula: FormulaSchema, payload: Dict[str, Any]) -> List[str]:
        """
        Checks if required engines actually populated data.
        """
        warnings = []
        for engine in formula.required_engines:
            engine_key = engine.replace("Engine", "").lower()
            if engine_key == "natalpromise":
                engine_key = "natal_promise"
                
            # Allow flexible matching for engine keys
            found = False
            for k in payload.keys():
                if engine_key in k.lower():
                    found = True
                    break
                    
            if not found:
                warnings.append(f"Engine Degradation: {engine} output is missing.")
        return warnings

    @staticmethod
    def evaluate(formula: FormulaSchema, engine_outputs: Dict[str, Any], isolated_signals: Dict[str, Any]) -> FormulaEvaluationResult:
        # Convert response to dict for extraction
        if isinstance(engine_outputs, dict):
            payload = engine_outputs
        else:
            try:
                payload = engine_outputs.model_dump()
            except AttributeError:
                payload = dict(engine_outputs)
            
        system_warnings = FormulaEvaluator.check_engine_degradation(formula, payload)
        
        # Missing payload handling (Risk-FR-05)
        for sig in formula.required_signals:
            if sig not in isolated_signals:
                system_warnings.append(f"Missing Payload: requested signal '{sig}' not found.")
        
        # Boolean condition evaluation
        fulfilled_layers = 0
        total_layers = len(formula.required_confidence_layers)
        
        for layer in formula.required_confidence_layers:
            is_fulfilled = True
            
            # Simulated boolean mapping: if degradation impacts the layer, mark False
            if "dasha" in layer.lower() and any("DashaEngine" in w for w in system_warnings):
                is_fulfilled = False
                
            if is_fulfilled:
                fulfilled_layers += 1
                
        # Domain prefix mapping to extract accurate promise score
        PREFIX_TO_DOMAIN = {
            "MAR": "marriage", "CAR": "career", "WEA": "wealth",
            "AST": "property", "EDU": "education", "FAM": "children",
            "HLT": "health", "LIT": "litigation", "TRV": "travel",
            "SPR": "spirituality", "REL": "compatibility"
        }
        domain_prefix = formula.formula_key.split("_")[0]
        domain_name = PREFIX_TO_DOMAIN.get(domain_prefix)
        promise_score = payload.get("natal_promise", {}).get(domain_name, {}).get("score", 50) if domain_name else 50
        
        # Confidence layer evaluation & Matrix Resolution (Pure Boolean Gating)
        final_state = "MIXED"
        is_degraded = len(system_warnings) > 0
        
        if total_layers > 0:
            if is_degraded:
                final_state = "MIXED"  # Force neutral if degraded
            elif fulfilled_layers == total_layers:
                final_state = "FAVORABLE"
            elif fulfilled_layers == 0:
                final_state = "UNFAVORABLE"
            else:
                final_state = "MIXED"
                
        # Primary Promise Gate Application (Hard Governance)
        if promise_score < 35:
            final_state = "UNFAVORABLE"
        elif promise_score < 50 and final_state == "FAVORABLE":
            final_state = "MIXED"
        
        return FormulaEvaluationResult(
            final_state=final_state,
            isolated_signals=isolated_signals,
            answer_template_key=formula.answer_template_key,
            system_warnings=system_warnings
        )
