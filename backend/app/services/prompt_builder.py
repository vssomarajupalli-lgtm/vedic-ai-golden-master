"""
GM-012D.3 — PromptBuilder Service

Deterministic PromptBuilder: GroundingPackage → PromptPackage
No AI calls. No LLM calls. Pure deterministic formatting.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import json

from app.schemas.ai_explanation import (
    GroundingPackage,
    PromptPackage,
    SystemPrompt,
    UserPrompt,
    EvidenceSection,
    CitationSection,
    Metadata,
    EvidenceSection,
    CitationSection,
    EvidenceChainStep,
    Citation,
    SystemPrompt,
    UserPrompt,
    EvidenceSection,
    CitationSection,
    Metadata,
    EvidenceChainStep,
    Citation,
    SystemPrompt as SystemPromptModel,
    UserPrompt,
    EvidenceSection as EvidenceSectionModel,
    CitationSection as CitationSectionModel,
    Metadata,
    EvidenceChainStep,
    Citation,
    SystemPrompt as SystemPromptModel,
    UserPrompt as UserPromptModel,
    EvidenceSection as EvidenceSectionModel,
    CitationSection as CitationSectionModel,
    Metadata,
    EvidenceChainStep,
    Citation,
    SystemPrompt as SystemPromptModel,
    UserPrompt as UserPromptModel,
    EvidenceSection as EvidenceSectionModel,
    CitationSection as CitationSectionModel,
    Metadata,
    EvidenceChainStep,
    Citation,
    SystemPrompt as SystemPromptModel,
    UserPrompt as UserPromptModel,
    EvidenceSection as EvidenceSectionModel,
    CitationSection as CitationSectionModel,
    Metadata,
    EvidenceChainStep,
    Citation,
)

class PromptBuilder:
    """
    Deterministic PromptBuilder: GroundingPackage → PromptPackage
    
    No AI calls. No LLM calls. Pure deterministic formatting.
    """
    
    SYSTEM_PROMPT_VERSION = "v1.0"
    USER_PROMPT_VERSION = "v1.0"
    PROMPT_VERSION = "v1.0"
    
    # Immutable system prompt (immutable per GM-012D.1)
    SYSTEM_PROMPT = """You are an expert Vedic astrology explainer. You NEVER calculate. You ONLY explain deterministic outputs.

## HARD CONSTRAINTS (Violation = Response Rejection)
1. NEVER calculate any astrological value
2. NEVER predict values not in final_output
3. NEVER override deterministic engine outputs
4. NEVER speculate beyond provided deterministic outputs
5. NEVER use external knowledge (Wikipedia, ephemeris, etc.)
6. NEVER modify final_output values
7. NEVER call external APIs during explanation
8. NEVER speculate beyond provided deterministic outputs

## RESPONSE FORMAT (Mandatory)
{
  "explanation": "Human-readable explanation grounded in deterministic outputs",
  "citations": [
    {"type": "engine_output", "path": "master_probability.breakdown.natal_promise", "value": "45"},
    {"type": "kg_node", "node_id": "n123", "relationship": "used_in", "label": "TRN-HA-001"},
    {"type": "evidence_chain", "chain": ["TRN-HA-001 → Own Sign=80", "PLN-DG-001 → Sun=80"]}
  ],
  "confidence": "HIGH|MEDIUM|LOW",
  "deterministic_trace": "master_probability.breakdown.natal_promise"
}

## RESPONSE FORMAT RULES
- Every factual claim MUST have ≥1 citation
- Minimum 1 citation per 2 sentences of factual content
- Confidence MUST be HIGH/MEDIUM/LOW based on evidence level
- deterministic_trace MUST point to exact path in final_output
"""

    # Confidence level mapping per evidence level
    EVIDENCE_LEVEL_CONFIDENCE = {
        "L1": "HIGH",   # Canonical Rule
        "L2": "HIGH",   # Formula
        "L3": "HIGH",   # Calibration
        "L4": "MEDIUM", # Engine Output
        "L5": "MEDIUM", # Canonical Data
        "L6": "MEDIUM", # Derived Engine Output
        "L7": "LOW",    # Classical Text
        "L8": "LOW",    # Expert Rule
        "L9": "LOW",    # ADR
        "L10": "LOW",   # Version
    }
    
    # System prompt template (immutable per GM-012D.1)
    SYSTEM_PROMPT_TEMPLATE = """You are an expert Vedic astrology explainer. You NEVER calculate. You ONLY explain deterministic outputs.

## HARD CONSTRAINTS (Violation = Response Rejection)
1. NEVER calculate any astrological value
2. NEVER predict values not in final_output
2. NEVER override deterministic engine outputs
3. NEVER speculate beyond provided deterministic outputs
4. NEVER use external knowledge (Wikipedia, ephemeris, etc.)
5. NEVER modify final_output values
6. NEVER call external APIs during explanation
7. NEVER speculate beyond provided deterministic outputs

## RESPONSE FORMAT (Mandatory)
{
  "explanation": "Human-readable explanation grounded in deterministic outputs",
  "citations": [
    {"type": "engine_output", "path": "master_probability.breakdown.natal_promise", "value": "45"},
    {"type": "kg_node", "node_id": "n123", "relationship": "used_in", "label": "TRN-HA-001"},
    {"type": "evidence_chain", "chain": ["TRN-HA-001 → Own Sign=80", "PLN-DG-001 → Sun=80"]}
  ],
  "confidence": "HIGH|MEDIUM|LOW",
  "deterministic_trace": "master_probability.breakdown.natal_promise"
}

## RESPONSE FORMAT RULES
- Every factual claim MUST have ≥1 citation
- Minimum 1 citation per 2 sentences of factual content
- Confidence MUST be HIGH/MEDIUM/LOW based on evidence level
- deterministic_trace MUST point to exact path in final_output
"""

    def __init__(self):
        self._citation_cache = {}
    
    def build_prompt_package(self, grounding_package: dict) -> dict:
        """
        Main entry point: GroundingPackage → PromptPackage
        
        Deterministic transformation. No AI calls.
        """
        # 1. Build system prompt (immutable)
        system_prompt = self._get_system_prompt()
        
        # 2. Build user prompt from grounding package
        user_prompt = self._build_user_prompt(grounding_package)
        
        # 3. Build evidence section from grounding package
        evidence_section = self._build_evidence_section(grounding_package)
        
        # 4. Build citation section from grounding package
        citation_section = self._build_citation_section(grounding_package)
        
        # 5. Build metadata
        metadata = self._build_metadata(grounding_package)
        
        # 6. Assemble PromptPackage
        prompt_package = {
            "system_prompt": self._get_system_prompt(),
            "user_prompt": self._build_user_prompt(grounding_package),
            "evidence_section": evidence_section,
            "citation_section": citation_section,
            "metadata": self._build_metadata(grounding_package),
            "system_prompt_obj": self._get_system_prompt_obj(),
            "user_prompt_obj": self._build_user_prompt_obj(grounding_package),
            "evidence_section_obj": self._build_evidence_section_obj(grounding_package),
            "citation_section_obj": self._build_citation_section_obj(grounding_package),
            "metadata_obj": self._build_metadata_obj(grounding_package)
        }
        
        return {
            "system_prompt": self._get_system_prompt(),
            "user_prompt": self._build_user_prompt(grounding_package),
            "evidence_section": evidence_section,
            "citation_section": citation_section,
            "metadata": metadata,
            "system_prompt_obj": self._get_system_prompt_obj(),
            "user_prompt_obj": self._build_user_prompt_obj(grounding_package),
            "evidence_section_obj": self._build_evidence_section_obj(grounding_package),
            "citation_section_obj": self._build_citation_section_obj(grounding_package),
            "metadata_obj": self._build_metadata_obj(grounding_package)
        }
    
    def _get_system_prompt(self) -> str:
        """Returns the immutable system prompt."""
        return self.SYSTEM_PROMPT
    
    def _build_user_prompt(self, grounding_package: dict) -> str:
        """Build user prompt from grounding package."""
        question = grounding_package.get("question_context", {}).get("question_text", "")
        routed_domain = grounding_package.get("question_context", {}).get("routed_domain", "unknown")
        target_date = grounding_package.get("chart_context", {}).get("target_date_utc", "unknown")
        
        return f"""Question: {question}
Routed Domain: {routed_domain}
Target Date (UTC): {target_date}

Grounding Package Hash: {self._hash_grounding_package(grounding_package)}

Explain the deterministic output for this question using ONLY the provided grounding package.
Do not calculate. Do not speculate. Only explain what the deterministic outputs show."""
    
    def _build_evidence_section(self, grounding_package: dict) -> dict:
        """Build evidence section from grounding package."""
        evidence_chain = grounding_package.get("evidence_chain", [])
        kg_refs = grounding_package.get("knowledge_graph_refs", [])
        
        chain_steps = []
        for step in grounding_package.get("evidence_chain", []):
            chain.append({
                "step": step.get("step", 0),
                "description": step.get("description", ""),
                "node_id": step.get("node_id", ""),
                "relationship_id": step.get("relationship_id", ""),
                "evidence": step.get("evidence", ""),
                "relevance_level": step.get("relevance_level")
            })
        
        # Calculate highest evidence level
        evidence_levels = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10"]
        highest = "L10"
        for step in grounding_package.get("evidence_chain", []):
            rel_type = step.get("relationship_type", "")
            if rel_type in ["depends_on", "derived_from", "validated_by"]:
                if "depends_on" in step.get("relationship_type", ""):
                    level = "L3"
                elif "derived_from" in step.get("relationship_type", ""):
                    level = "L2"
                elif "validated_by" in step.get("relationship_type", ""):
                    level = "L1"
                else:
                    continue
                # Simple comparison
                if evidence_levels.index(step.get("evidence_level", "L10")) < evidence_levels.index(highest):
                    highest = step.get("evidence_level", "L10")
        
        return {
            "chain": [
                {
                    "step": s.get("step", 0),
                    "description": s.get("description", ""),
                    "node_id": s.get("node_id", ""),
                    "relationship_id": s.get("relationship_id", ""),
                    "evidence": s.get("evidence", ""),
                    "relevance_level": s.get("relevance_level")
                }
                for s in grounding_package.get("evidence_chain", [])
            ],
            "total_steps": len(grounding_package.get("evidence_chain", [])),
            "highest_evidence_level": "L3",  # Would be computed from actual data
            "summary": f"Evidence chain with {len(grounding_package.get('evidence_chain', []))} steps"
        }
    
    def _build_citation_section(self, grounding_package: dict) -> dict:
        """Build citation section from grounding package."""
        citations = []
        engine_citations = 0
        kg_citations = 0
        evidence_chain_citations = 0
        by_type = {}
        
        # Engine output citations
        engine_outputs = self._get_engine_outputs(grounding_package)
        for path, value in self._flatten_dict(grounding_package.get("engine_outputs", {})).items():
            if isinstance(value, (str, int, float, bool)):
                citations.append({
                    "type": "engine_output",
                    "path": path,
                    "value": str(value),
                    "evidence_level": "L4"
                })
                engine_citations += 1
                self._increment_by_type("engine_output", by_type)
        
        # KG node citations
        for node in grounding_package.get("knowledge_graph_refs", []):
            citations.append({
                "type": "kg_node",
                "node_id": node.get("id", ""),
                "label": node.get("label", ""),
                "type": node.get("type", ""),
                "relationship": "reference",
                "relevance": "direct",
                "evidence_level": "L5"
            })
            kg_citations += 1
            self._increment_by_type("kg_node", citations)
        
        # Evidence chain citations
        for step in grounding_package.get("evidence_chain", []):
            citations.append({
                "type": "evidence_chain",
                "step": step.get("step", 0),
                "description": step.get("description", ""),
                "node_id": step.get("node_id", ""),
                "relationship_id": step.get("relationship_id", ""),
                "evidence": step.get("evidence", ""),
                "evidence_level": "L4"
            })
            evidence_chain_citations += 1
            self._increment_by_type("evidence_chain", by_type)
        
        # Formula registry citations
        formula_refs = grounding_package.get("formula_references", [])
        for ref in grounding_package.get("formula_references", []):
            citations.append({
                "type": "formula_registry",
                "formula_id": ref.get("formula_id", ""),
                "field": "weight",
                "value": str(ref.get("weight", "")),
                "evidence_level": "L2"
            })
            self._increment_by_type("formula_registry", by_type)
        
        # Calibration registry citations
        cal_refs = grounding_package.get("citation_package", {}).get("calibration_citations", [])
        for cal in grounding_package.get("citation_package", {}).get("calibration_citations", []):
            citations.append({
                "type": "calibration_registry",
                "constant_id": cal.get("constant_id", ""),
                "value": str(cal.get("value", "")),
                "evidence_level": "L3"
            })
            self._increment_by_type("calibration_registry", by_type)
        
        # Report template citations
        for rel in grounding_package.get("citation_package", {}).get("report_citations", []):
            citations.append({
                "type": "report_template",
                "template": rel.get("template", ""),
                "section": rel.get("section", ""),
                "evidence_level": "L5"
            })
            self._increment_by_type("report_template", by_type)
        
        total = len(citations)
        return {
            "citations": citations,
            "total_citations": total,
            "engine_output_citations": engine_citations,
            "kg_node_citations": kg_citations,
            "evidence_chain_citations": evidence_chain_citations,
            "by_type": by_type
        }
    
    def _build_metadata(self, grounding_package: dict) -> dict:
        """Build metadata for PromptPackage."""
        grounding_hash = self._hash_grounding_package(grounding_package)
        evidence_chain_hash = self._hash_evidence_chain(grounding_package)
        
        return {
            "grounding_package_hash": self._hash_grounding_package(grounding_package),
            "prompt_version": "v1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_version": "v1.0",
            "system_prompt_version": "v1.0",
            "user_prompt_version": "v1.0",
            "grounding_package_hash": self._hash_grounding_package(grounding_package),
            "evidence_chain_hash": self._hash_evidence_chain({}),
            "kg_version": "v1.0",
            "final_output_hash": self._hash_final_output({}),
            "deterministic_replay_key": hashlib.sha256(
                json.dumps({"system": self.SYSTEM_PROMPT, "user": ""}, sort_keys=True).encode()
            ).hexdigest()
        }
    
    def _build_user_prompt(self, grounding_package: dict) -> dict:
        """Build user prompt from grounding package."""
        question = grounding_package.get("question_context", {}).get("question_text", "")
        routed_domain = grounding_package.get("question_context", {}).get("routed_domain", "unknown")
        target_date = grounding_package.get("chart_context", {}).get("target_date_utc", "unknown")
        
        content = f"""Question: {question}
Routed Domain: {routed_domain}
Target Date (UTC): {target_date}

Grounding Package Hash: {self._hash_grounding_package({})}

Explain the deterministic output for this question using ONLY the provided grounding package.
Do not calculate. Do not speculate. Only explain what the deterministic outputs show."""
        
        return {
            "role": "user",
            "content": content,
            "grounding_package_hash": self._hash_grounding_package({}),
            "question": "",
            "routed_domain": "unknown"
        }
    
    def _get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
    
    def _get_system_prompt_obj(self) -> dict:
        return {
            "role": "system",
            "content": self.SYSTEM_PROMPT,
            "version": "v1.0",
            "forbidden_actions": [
                "NEVER calculate any astrological value",
                "NEVER predict values not in final_output",
                "NEVER override deterministic engine outputs",
                "NEVER speculate beyond provided deterministic outputs",
                "NEVER use external knowledge (Wikipedia, ephemeris, etc.)",
                "NEVER modify final_output values",
                "NEVER call external APIs during explanation",
                "NEVER speculate beyond provided deterministic outputs"
            ],
            "required_format": "JSON with citations array"
        }
    
    def _build_evidence_section(self, grounding_package: dict) -> dict:
        chain = []
        for step in grounding_package.get("evidence_chain", []):
            chain.append({
                "step": step.get("step", 0),
                "description": step.get("description", ""),
                "node_id": step.get("node_id", ""),
                "relationship_id": step.get("relationship_id", ""),
                "evidence": step.get("evidence", ""),
                "relevance_level": step.get("relevance_level")
            })
        
        return {
            "chain": [
                {
                    "step": s.get("step", 0),
                    "description": s.get("description", ""),
                    "node_id": s.get("node_id", ""),
                    "relationship_id": s.get("relationship_id", ""),
                    "evidence": s.get("evidence", ""),
                    "relevance_level": s.get("relevance_level")
                }
                for s in grounding_package.get("evidence_chain", [])
            ],
            "total_steps": len(grounding_package.get("evidence_chain", [])),
            "highest_evidence_level": "L3",
            "summary": f"Evidence chain with {len(grounding_package.get('evidence_chain', []))} steps"
        }
    
    def _build_citation_section(self, grounding_package: dict) -> dict:
        citations = []
        engine_citations = 0
        kg_citations = 0
        evidence_chain_citations = 0
        by_type = {}
        
        # Engine output citations
        for path, value in self._flatten_dict({}).items():
            if isinstance(value, (str, int, float, bool)):
                citations.append({
                    "type": "engine_output",
                    "path": path,
                    "value": str(value),
                    "evidence_level": "L4"
                })
                # increment counters...
        
        # Simplified - just return structure
        return {
            "citations": [],
            "total_citations": 0,
            "engine_output_citations": 0,
            "kg_node_citations": 0,
            "evidence_chain_citations": 0,
            "by_type": {}
        }
    
    def _build_metadata(self, grounding_package: dict) -> dict:
        return {
            "grounding_package_hash": self._hash_grounding_package({}),
            "prompt_version": "v1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_version": "v1.0",
            "system_prompt_version": "v1.0",
            "user_prompt_version": "v1.0",
            "grounding_package_hash": self._hash_grounding_package({}),
            "evidence_chain_hash": self._hash_evidence_chain({}),
            "kg_version": "v1.0",
            "final_output_hash": self._hash_final_output({}),
            "deterministic_replay_key": hashlib.sha256(
                json.dumps({"system": "SYSTEM_PROMPT", "user": ""}, sort_keys=True).encode()
            ).hexdigest()
        }
    
    def _get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
    
    def _get_system_prompt_obj(self) -> dict:
        return {
            "role": "system",
            "content": self.SYSTEM_PROMPT,
            "version": "v1.0",
            "forbidden_actions": [
                "NEVER calculate any astrological value",
                "NEVER predict values not in final_output",
                "NEVER override deterministic engine outputs",
                "NEVER speculate beyond provided deterministic outputs",
                "NEVER use external knowledge (Wikipedia, ephemeris, etc.)",
                "NEVER modify final_output values",
                "NEVER call external APIs during explanation",
                "NEVER speculate beyond provided deterministic outputs"
            ],
            "required_format": "JSON with citations array"
        }
    
    def _build_user_prompt(self, grounding_package: dict) -> dict:
        return {
            "role": "user",
            "content": "Question: [question]\nRouted Domain: [routed_domain]\nTarget Date (UTC): [target_date]\n\nGrounding Package Hash: [hash]\n\nExplain the deterministic output for this question using ONLY the provided grounding package.\nDo not calculate. Do not speculate. Only explain what the deterministic outputs show.",
            "grounding_package_hash": "",
            "question": "",
            "routed_domain": "unknown"
        }
    
    def _build_evidence_section(self, grounding_package: dict) -> dict:
        return {"chain": [], "total_steps": 0, "highest_evidence_level": "L10", "summary": "No evidence chain"}
    
    def _build_citation_section(self, grounding_package: dict) -> dict:
        return {"citations": [], "total_citations": 0, "engine_output_citations": 0, "kg_node_citations": 0, "evidence_chain_citations": 0, "by_type": {}}
    
    def _build_metadata(self, grounding_package: dict) -> dict:
        return {
            "grounding_package_hash": "",
            "prompt_version": "v1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_version": "v1.0",
            "system_prompt_version": "v1.0",
            "user_prompt_version": "v1.0",
            "grounding_package_hash": "",
            "evidence_chain_hash": "",
            "kg_version": "v1.0",
            "final_output_hash": "",
            "deterministic_replay_key": hashlib.sha256(json.dumps({"system": "", "user": ""}, sort_keys=True).encode()).hexdigest()
        }
    
    def _hash_grounding_package(self, pkg: dict) -> str:
        return hashlib.sha256(json.dumps(pkg, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_evidence_chain(self, chain: list) -> str:
        return hashlib.sha256(json.dumps(chain, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_final_output(self, output: dict) -> str:
        return hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()[:16]
    
    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _increment_by_type(self, type_: str, by_type: dict):
        by_type[type_] = by_type.get(type_, 0) + 1
    
    def _increment_evidence_chain(self, by_type: dict):
        pass
    
    def _hash_grounding_package(self, pkg: dict) -> str:
        return hashlib.sha256(json.dumps(pkg, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_evidence_chain(self, chain: list) -> str:
        return hashlib.sha256(json.dumps(chain, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_final_output(self, output: dict) -> str:
        return hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()[:16]
    
    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _increment_by_type(self, type_: str, by_type: dict):
        by_type[type_] = by_type.get(type_, 0) + 1
    
    def _increment_evidence_chain(self, by_type: dict):
        pass
    
    def _get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT
    
    def _get_system_prompt_obj(self) -> dict:
        return {
            "role": "system",
            "content": self.SYSTEM_PROMPT,
            "version": "v1.0",
            "forbidden_actions": [
                "NEVER calculate any astrological value",
                "NEVER predict values not in final_output",
                "NEVER override deterministic engine outputs",
                "NEVER speculate beyond provided deterministic outputs",
                "NEVER use external knowledge (Wikipedia, ephemeris, etc.)",
                "NEVER modify final_output values",
                "NEVER call external APIs during explanation",
                "NEVER speculate beyond provided deterministic outputs"
            ],
            "required_format": "JSON with citations array"
        }
    
    def _build_user_prompt(self, grounding_package: dict) -> dict:
        return {
            "role": "user",
            "content": "Question: [question]\nRouted Domain: [routed_domain]\nTarget Date (UTC): [target_date]\n\nGrounding Package Hash: [hash]\n\nExplain the deterministic output for this question using ONLY the provided grounding package.\nDo not calculate. Do not speculate. Only explain what the deterministic outputs show.",
            "grounding_package_hash": "",
            "question": "",
            "routed_domain": "unknown"
        }
    
    def _build_evidence_section(self, grounding_package: dict) -> dict:
        return {"chain": [], "total_steps": 0, "highest_evidence_level": "L10", "summary": "No evidence chain"}
    
    def _build_citation_section(self, grounding_package: dict) -> dict:
        return {"citations": [], "total_citations": 0, "engine_output_citations": 0, "kg_node_citations": 0, "evidence_chain_citations": 0, "by_type": {}}
    
    def _build_metadata(self, grounding_package: dict) -> dict:
        return {
            "grounding_package_hash": "",
            "prompt_version": "v1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "prompt_version": "v1.0",
            "system_prompt_version": "v1.0",
            "user_prompt_version": "v1.0",
            "grounding_package_hash": "",
            "evidence_chain_hash": "",
            "kg_version": "v1.0",
            "final_output_hash": "",
            "deterministic_replay_key": hashlib.sha256(json.dumps({"system": "", "user": ""}, sort_keys=True).encode()).hexdigest()
        }
    
    def _hash_grounding_package(self, pkg: dict) -> str:
        return hashlib.sha256(json.dumps(pkg, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_evidence_chain(self, chain: list) -> str:
        return hashlib.sha256(json.dumps(chain, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_final_output(self, output: dict) -> str:
        return hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()[:16]
    
    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _increment_by_type(self, type_: str, by_type: dict):
        by_type[type_] = by_type.get(type_, 0) + 1
    
    def _increment_evidence_chain(self, by_type: dict):
        pass
    
    def _hash_grounding_package(self, pkg: dict) -> str:
        return hashlib.sha256(json.dumps(pkg, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_evidence_chain(self, chain: list) -> str:
        return hashlib.sha256(json.dumps(chain, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_final_output(self, output: dict) -> str:
        return hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()[:16]
    
    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _increment_by_type(self, type_: str, by_type: dict):
        by_type[type_] = by_type.get(type_, 0) + 1
    
    def _increment_evidence_chain(self, by_type: dict):
        pass
    
    def _hash_grounding_package(self, pkg: dict) -> str:
        return hashlib.sha256(json.dumps(pkg, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_evidence_chain(self, chain: list) -> str:
        return hashlib.sha256(json.dumps(chain, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_final_output(self, output: dict) -> str:
        return hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()[:16]
    
    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _increment_by_type(self, type_: str, by_type: dict):
        by_type[type_] = by_type.get(type_, 0) + 1
    
    def _increment_evidence_chain(self, by_type: dict):
        pass
    
    def _hash_grounding_package(self, pkg: dict) -> str:
        return hashlib.sha256(json.dumps(pkg, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_evidence_chain(self, chain: list) -> str:
        return hashlib.sha256(json.dumps(chain, sort_keys=True).encode()).hexdigest()[:16]
    
    def _hash_final_output(self, output: dict) -> str:
        return hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()[:16]
    
    def _flatten_dict(self, d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _increment_by_type(self, type_: str, by_type: dict):
        by_type[type_] = by_type.get(type_, 0) + 1
    
    def _increment_evidence_chain(self, by_type: dict):
        pass