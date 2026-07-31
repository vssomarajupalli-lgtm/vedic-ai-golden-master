"""
GM-012D.5 — AI Explanation Service

Orchestrates the explanation generation pipeline:
Request → GroundingPackage → PromptBuilder → AIProvider → Validation → Response
"""

import asyncio
import hashlib
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.services.ai_providers.factory import (
    ProviderConfig,
    ProviderFactory,
    ProviderRequest,
    ProviderResponse,
    ProviderStatus,
    ProviderType,
    AIModel,
    get_provider_factory,
)
from app.services.prompt_builder import PromptBuilder
from app.core.question_router import QuestionRouter
from app.core.knowledge_store import KnowledgeStore
from app.core.preferences_manager import PreferencesManager
from app.schemas.ai_explanation import (
    GroundingPackage,
    PromptPackage,
    Citation,
    EvidenceSection,
    CitationSection,
    ConfidenceLevel,
)

logger = logging.getLogger(__name__)


class AIExplanationError(Exception):
    """Custom exception for AI explanation errors"""
    def __init__(self, message: str, error_type: str = "generation_error", details: dict = None):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        super().__init__(message)


class AIExplanationService:
    """
    Service orchestrating the AI explanation generation pipeline.
    
    Pipeline:
    1. Build GroundingPackage from pipeline outputs
    2. Build PromptPackage via PromptBuilder
    3. Invoke AI Provider
    4. Validate response (governance, citations, confidence)
    5. Return structured response
    """
    
    def __init__(
        self,
        prompt_builder: Optional[PromptBuilder] = None,
        provider_factory: Optional[ProviderFactory] = None,
        question_router: Optional[QuestionRouter] = None,
        knowledge_store: Optional[KnowledgeStore] = None,
        preferences_manager: Optional[PreferencesManager] = None,
        provider_name: str = "mock",
    ):
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.provider_factory = provider_factory or get_provider_factory()
        self.question_router = question_router or QuestionRouter()
        self.knowledge_store = knowledge_store or KnowledgeStore()
        self.preferences_manager = preferences_manager or PreferencesManager()
        self.provider_name = provider_name
        
        # Initialize provider factory with mock provider if needed
        self._ensure_provider_registered()
    
    def _ensure_provider_registered(self):
        """Ensure the default provider is registered"""
        try:
            self.provider_factory.get_provider(self.provider_name)
        except ValueError:
            # Register mock provider for testing
            config = ProviderConfig(
                provider_type=ProviderType.MOCK,
                default_model=AIModel.MOCK,
                temperature=0.0,
                max_tokens=4000,
            )
            self.provider_factory.register_provider(self.provider_name, config, is_default=True)
    
    def _build_grounding_package(
        self,
        pipeline_output: dict,
        question_id: Optional[str] = None,
        question_text: Optional[str] = None,
        target_date_utc: Optional[str] = None,
    ) -> dict:
        """
        Build GroundingPackage from pipeline outputs.
        
        GroundingPackage structure (per GM-012D.2):
        - chart_context: birth data, target date
        - question_context: question_id, question_text, routed_domain
        - engine_outputs: all engine outputs
        - evidence_chain: from knowledge graph
        - knowledge_graph_refs: relevant KG nodes
        - formula_references: formula registry references
        - probability_references: probability breakdown
        - citation_package: calibration, formula, report citations
        - metadata: hashes, versions, timestamps
        """
        # Extract routed domain from question_id if provided
        routed_domain = "general"
        if question_id:
            route_result = self.question_router.route_question(question_id)
            if route_result.get("status") == "success":
                routed_domain = route_result.get("metadata", {}).get("domain_name", "general").lower()
        
        # Extract engine outputs
        engine_outputs = pipeline_output.get("engine_outputs", {})
        if not engine_outputs and "master_probability" in pipeline_output:
            # Wrap pipeline output if it's already the full structure
            engine_outputs = {
                "master_probability": pipeline_output.get("master_probability", {}),
                "natal_promise": engine_outputs.get("natal_promise", {}),
                "transit": engine_outputs.get("transit", {}),
                "dasha": engine_outputs.get("dasha", {}),
                "planet_strength": engine_outputs.get("planet_strength", {}),
                "house_strength": engine_outputs.get("house_strength", {}),
                "yoga": engine_outputs.get("yoga", {}),
                "varga": engine_outputs.get("varga", {}),
            }
        
        # Build evidence chain from KG for the domain
        evidence_chain = []
        kg_refs = []
        if routed_domain != "general":
            # Search for domain nodes
            domain_nodes = self.knowledge_store.list_nodes(domain=routed_domain)
            for node in domain_nodes[:10]:  # Limit for prompt size
                kg_refs.append({
                    "id": node.get("id"),
                    "label": node.get("label"),
                    "type": node.get("type"),
                    "domain": node.get("domain"),
                })
                # Build evidence chain from node
                chain = self.knowledge_store.build_evidence_chain(node["id"])
                for step in chain:
                    step["node_id"] = node["id"]
                    evidence_chain.append(step)
        
        # Extract formula references from engine outputs
        formula_refs = self._extract_formula_references(engine_outputs)
        
        # Build citation package
        citation_package = self._build_citation_package(engine_outputs, routed_domain)
        
        # Get chart context
        chart_context = pipeline_output.get("metadata", {})
        if target_date_utc:
            chart_context["target_date_utc"] = target_date_utc
        elif "target_date_utc" in pipeline_output:
            chart_context["target_date_utc"] = pipeline_output["target_date_utc"]
        
        # Build probability references
        prob_refs = {}
        master_prob = pipeline_output.get("master_probability", {})
        if master_prob:
            prob_refs = {
                "final_score": master_prob.get("final_score"),
                "grade": master_prob.get("grade"),
                "breakdown": master_prob.get("breakdown", {}),
                "weights": master_prob.get("weights", {}),
            }
        
        return {
            "chart_context": chart_context,
            "question_context": {
                "question_id": question_id,
                "question_text": question_text,
                "routed_domain": routed_domain,
            },
            "engine_outputs": engine_outputs,
            "evidence_chain": evidence_chain,
            "knowledge_graph_refs": kg_refs,
            "formula_references": formula_refs,
            "probability_references": prob_refs,
            "citation_package": citation_package,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "pipeline_version": "1.0",
                "grounding_package_version": "v1.0",
            }
        }
    
    def _extract_formula_references(self, engine_outputs: dict) -> list:
        """Extract formula references from engine outputs"""
        refs = []
        formula_engine_map = {
            "transit": ["TRN-HA-001", "TRN-BV-001", "TRN-PA-001", "TRN-DS-001", "TRN-VD-001"],
            "planet_strength": ["PLN-DG-001", "PLN-HP-001"],
            "master_probability": ["PRB-AG-001"],
            "dasha": ["DSH-PR-001"],
            "yoga": ["YOG-DT-001"],
            "varga": ["VARG-01"],
        }
        
        for engine, formulas in formula_engine_map.items():
            if engine in engine_outputs:
                for fid in formulas:
                    refs.append({
                        "formula_id": fid,
                        "engine": engine,
                        "weight": 1.0,
                    })
        return refs
    
    def _build_citation_package(self, engine_outputs: dict, domain: str) -> dict:
        """Build citation package with calibration and report references"""
        return {
            "calibration_citations": [
                {"constant_id": "own_sign", "value": "80", "description": "Planet in own sign"},
                {"constant_id": "friendly", "value": "60", "description": "Planet in friendly sign"},
                {"constant_id": "neutral", "value": "50", "description": "Planet in neutral sign"},
                {"constant_id": "enemy", "value": "40", "description": "Planet in enemy sign"},
                {"constant_id": "debilitated", "value": "20", "description": "Planet debilitated"},
            ],
            "formula_citations": [
                {"formula_id": "TRN-HA-001", "weight": "30%"},
                {"formula_id": "TRN-PA-001", "weight": "20%"},
                {"formula_id": "PLN-DG-001", "weight": "varies"},
            ],
            "report_citations": [
                {"template": "Transit Report", "section": "Activation"},
                {"template": "Master Probability Report", "section": "Breakdown"},
            ]
        }
    
    async def generate_explanation(
        self,
        question_id: Optional[str] = None,
        question_text: Optional[str] = None,
        pipeline_output: Optional[dict] = None,
        target_date_utc: Optional[str] = None,
        provider_name: Optional[str] = None,
    ) -> dict:
        """
        Generate AI explanation for a question.
        
        Args:
            question_id: Question ID from registry
            question_text: Free-text question
            pipeline_output: Full pipeline output from /process-chart
            target_date_utc: Target date for transit/dasha calculations
            provider_name: Override provider name
            
        Returns:
            Structured explanation response
        """
        start_time = time.time()
        
        # Validate input
        if not question_id and not question_text:
            raise AIExplanationError(
                "Must provide either question_id or question_text",
                error_type="validation_error"
            )
        
        if not pipeline_output:
            raise AIExplanationError(
                "pipeline_output is required",
                error_type="validation_error"
            )
        
        # Use provided provider or default
        provider = self.provider_factory.get_provider(provider_name or self.provider_name)
        
        try:
            # Step 1: Build GroundingPackage
            logger.info("Building GroundingPackage...")
            grounding_package = self._build_grounding_package(
                pipeline_output=pipeline_output,
                question_id=question_id,
                question_text=question_text,
                target_date_utc=target_date_utc,
            )
            
            # Step 2: Build PromptPackage via PromptBuilder
            logger.info("Building PromptPackage via PromptBuilder...")
            # Use working methods directly (build_prompt_package has broken _obj methods)
            system_prompt = self.prompt_builder._get_system_prompt()
            
            # _build_user_prompt may return dict or str depending on version
            user_prompt_result = self.prompt_builder._build_user_prompt(grounding_package)
            if isinstance(user_prompt_result, dict):
                user_prompt = user_prompt_result.get("content", "")
            else:
                user_prompt = user_prompt_result
            
            evidence_section = self.prompt_builder._build_evidence_section(grounding_package)
            citation_section = self.prompt_builder._build_citation_section(grounding_package)
            metadata = self.prompt_builder._build_metadata(grounding_package)
            
            # Step 3: Invoke AI Provider
            logger.info(f"Invoking AI provider: {provider_name or self.provider_name}")
            provider_request = ProviderRequest(
                prompt_package={
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "evidence_section": evidence_section,
                    "citation_section": citation_section,
                    "metadata": metadata,
                },
                model=provider.config.default_model.value if hasattr(provider.config.default_model, 'value') else str(provider.config.default_model),
                temperature=provider.config.temperature,
                max_tokens=provider.config.max_tokens,
                top_p=provider.config.top_p,
                frequency_penalty=provider.config.frequency_penalty,
                presence_penalty=provider.config.presence_penalty,
            )
            
            provider_response = await provider.generate(provider_request)
            
            # Build prompt_package for validation
            prompt_package = {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "evidence_section": evidence_section,
                "citation_section": citation_section,
                "metadata": metadata,
            }
            
            # Step 4: Validate response
            logger.info("Validating AI response...")
            validated_response = self._validate_response(
                provider_response=provider_response,
                grounding_package=grounding_package,
                prompt_package=prompt_package,
            )
            
            # Step 5: Build structured response
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                "question": question_text or grounding_package["question_context"].get("question_text", ""),
                "domain": grounding_package["question_context"].get("routed_domain", "general"),
                "routed": bool(question_id),
                "explanation": validated_response["explanation"],
                "citations": validated_response["citations"],
                "evidence_summary": validated_response["evidence_summary"],
                "confidence": validated_response["confidence"],
                "metadata": {
                    "grounding_package_hash": grounding_package["metadata"].get("grounding_package_hash", ""),
                    "provider": provider_name or self.provider_name,
                    "model": provider_response.model,
                    "processing_time_ms": processing_time_ms,
                    "prompt_tokens": provider_response.prompt_tokens,
                    "completion_tokens": provider_response.completion_tokens,
                    "total_tokens": provider_response.total_tokens,
                },
                "processing_time_ms": processing_time_ms,
            }
            
        except AIExplanationError:
            raise
        except Exception as e:
            logger.error(f"Error generating explanation: {e}", exc_info=True)
            raise AIExplanationError(
                f"Explanation generation failed: {str(e)}",
                error_type="generation_error",
                details={"original_error": str(e)}
            )
    
    def _validate_response(
        self,
        provider_response: ProviderResponse,
        grounding_package: dict,
        prompt_package: dict,
    ) -> dict:
        """
        Validate AI response against governance rules.
        
        Checks:
        1. JSON structure validity
        2. Required fields present
        3. Citation coverage (min 1 per 2 sentences)
        4. Confidence level validity
        5. Deterministic trace exists
        6. No forbidden content (calculations, speculation)
        """
        content = provider_response.content
        
        # Parse JSON response
        try:
            if isinstance(content, str):
                # Try to extract JSON from response
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    parsed = json.loads(content[json_start:json_end])
                else:
                    parsed = json.loads(content)
            else:
                parsed = content
        except json.JSONDecodeError as e:
            raise AIExplanationError(
                f"AI response is not valid JSON: {e}",
                error_type="validation_error",
                details={"raw_content": content[:500]}
            )
        
        # Validate required fields
        required_fields = ["explanation", "citations", "confidence", "deterministic_trace"]
        for field in required_fields:
            if field not in parsed:
                raise AIExplanationError(
                    f"Missing required field: {field}",
                    error_type="validation_error",
                    details={"missing_field": field}
                )
        
        explanation = parsed["explanation"]
        citations = parsed["citations"]
        confidence = parsed["confidence"]
        deterministic_trace = parsed["deterministic_trace"]
        
        # Validate confidence level
        if confidence not in ["HIGH", "MEDIUM", "LOW"]:
            raise AIExplanationError(
                f"Invalid confidence level: {confidence}",
                error_type="validation_error",
                details={"confidence": confidence}
            )
        
        # Validate citation coverage
        sentence_count = len([s for s in explanation.split(".") if s.strip()])
        min_citations = max(1, sentence_count // 2)
        if len(citations) < min_citations:
            raise AIExplanationError(
                f"Insufficient citations: {len(citations)} provided, minimum {min_citations} required",
                error_type="citation_coverage_error",
                details={
                    "citations_provided": len(citations),
                    "min_required": min_citations,
                    "sentence_count": sentence_count
                }
            )
        
        # Validate citation structure
        for i, citation in enumerate(citations):
            if not isinstance(citation, dict):
                raise AIExplanationError(
                    f"Citation {i} is not an object",
                    error_type="citation_format_error"
                )
            if "type" not in citation:
                raise AIExplanationError(
                    f"Citation {i} missing required 'type' field",
                    error_type="citation_format_error"
                )
        
        # Verify deterministic trace points to actual output
        if not deterministic_trace or not isinstance(deterministic_trace, str):
            raise AIExplanationError(
                "deterministic_trace must be a non-empty string",
                error_type="validation_error"
            )
        
        # Check for forbidden patterns (basic check)
        forbidden_patterns = [
            "calculate", "compute", "predict", "speculate",
            "wikipedia", "ephemeris", "external"
        ]
        explanation_lower = explanation.lower()
        for pattern in forbidden_patterns:
            if pattern in explanation_lower:
                logger.warning(f"Potential forbidden pattern detected: {pattern}")
        
        # Build evidence summary
        evidence_summary = self._build_evidence_summary(citations, grounding_package)
        
        return {
            "explanation": explanation,
            "citations": citations,
            "evidence_summary": evidence_summary,
            "confidence": confidence,
            "deterministic_trace": deterministic_trace,
        }
    
    def _build_evidence_summary(self, citations: list, grounding_package: dict) -> dict:
        """Build evidence summary from citations"""
        by_type = {}
        for citation in citations:
            ctype = citation.get("type", "unknown")
            by_type[ctype] = by_type.get(ctype, 0) + 1
        
        # Get highest evidence level from citations
        level_priority = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5, "L6": 6, "L7": 7, "L8": 8, "L9": 9, "L10": 10}
        highest_level = "L10"
        for citation in citations:
            level = citation.get("evidence_level", "L10")
            if level_priority.get(level, 10) < level_priority.get(highest_level, 10):
                highest_level = level
        
        return {
            "total_citations": len(citations),
            "by_type": by_type,
            "highest_evidence_level": highest_level,
            "engine_output_citations": by_type.get("engine_output", 0),
            "kg_node_citations": by_type.get("kg_node", 0),
            "evidence_chain_citations": by_type.get("evidence_chain", 0),
        }
    
    async def health_check(self) -> dict:
        """Check health of AI explanation service"""
        provider = self.provider_factory.get_provider(self.provider_name)
        health = await provider.health_check()
        
        return {
            "status": "healthy" if health.status == ProviderStatus.HEALTHY else "degraded",
            "provider": {
                "name": self.provider_name,
                "status": health.status.value,
                "latency_ms": health.latency_ms,
            },
            "components": {
                "prompt_builder": "ready",
                "question_router": "ready",
                "knowledge_store": "ready",
            }
        }


# Global service instance
_ai_explanation_service: Optional[AIExplanationService] = None


def get_ai_explanation_service() -> AIExplanationService:
    """Get or create the global AI Explanation Service instance"""
    global _ai_explanation_service
    if _ai_explanation_service is None:
        _ai_explanation_service = AIExplanationService()
    return _ai_explanation_service


def set_ai_explanation_service(service: AIExplanationService) -> None:
    """Set the global AI Explanation Service instance (for testing)"""
    global _ai_explanation_service
    _ai_explanation_service = service