import json
from pathlib import Path
from typing import Optional
from app.formulas.schema import FormulaEvaluationResult, ComposerPromptPackage

class TemplateNotFoundError(Exception):
    pass

class AnswerComposer:
    def __init__(self, templates_dir: Optional[str] = None):
        if templates_dir is None:
            self.templates_dir = Path(__file__).parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)

    def _load_template(self, template_key: str, final_state: str) -> str:
        """
        Loads the strictly governed system prompt text file.
        """
        filename = f"{template_key}_{final_state.lower()}.txt"
        filepath = self.templates_dir / filename
        
        if not filepath.exists():
            raise TemplateNotFoundError(f"Template file not found: {filepath}")
            
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()

    def _build_evidence_block(self, result: FormulaEvaluationResult) -> str:
        """
        Deterministically transforms the JSON evidence into a strict string block.
        """
        evidence_lines = []
        evidence_lines.append(f"FINAL STATE: {result.final_state}")
        
        if result.system_warnings:
            evidence_lines.append("\nSYSTEM WARNINGS:")
            for warning in result.system_warnings:
                evidence_lines.append(f"- {warning}")
                
        evidence_lines.append("\nASTROLOGICAL EVIDENCE:")
        evidence_lines.append(json.dumps(result.isolated_signals, indent=2))
        
        return "\n".join(evidence_lines)

    def compose(self, result: FormulaEvaluationResult) -> ComposerPromptPackage:
        """
        Constructs the strict Prompt Package for future LLM execution.
        """
        system_prompt = self._load_template(result.answer_template_key, result.final_state)
        evidence_block = self._build_evidence_block(result)
        
        template_id = f"{result.answer_template_key}_{result.final_state.lower()}"
        
        return ComposerPromptPackage(
            prompt_template_id=template_id,
            system_prompt=system_prompt,
            user_prompt=None,  # explicitly null/deferred
            evidence_block=evidence_block,
            system_warnings=result.system_warnings,
            final_state=result.final_state
        )

# Global singleton
answer_composer = AnswerComposer()
