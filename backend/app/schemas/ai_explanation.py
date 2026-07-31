"""
GM-012D.3 — PromptBuilder Schemas

Strongly typed models for GroundingPackage → PromptPackage transformation.
These models define the deterministic PromptBuilder output.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class CitationType(str, Enum):
    ENGINE_OUTPUT = "engine_output"
    KG_NODE = "kg_node"
    EVIDENCE_CHAIN = "evidence_chain"
    FORMULA_REGISTRY = "formula_registry"
    CALIBRATION_REGISTRY = "calibration_registry"
    REPORT_TEMPLATE = "report_template"


class EvidenceLevel(str, Enum):
    L1 = "L1"   # Canonical Rule
    L2 = "L2"   # Formula
    L3 = "L3"   # Calibration
    L4 = "L4"   # Engine Output
    L5 = "L5"   # Canonical Data
    L6 = "L6"   # Derived Engine Output
    L7 = "L7"   # Classical Text
    L8 = "L8"   # Expert Rule
    L9 = "L9"   # ADR
    L10 = "L10"  # Version


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CitationType(str, Enum):
    ENGINE_OUTPUT = "engine_output"
    KG_NODE = "kg_node"
    EVIDENCE_CHAIN = "evidence_chain"
    FORMULA_REGISTRY = "formula_registry"
    CALIBRATION_REGISTRY = "calibration_registry"
    REPORT_TEMPLATE = "report_template"


class Citation(BaseModel):
    type: str
    path: Optional[str] = None
    value: Optional[str] = None
    node_id: Optional[str] = None
    relationship: Optional[str] = None
    label: Optional[str] = None
    chain: Optional[List[str]] = None
    formula_id: Optional[str] = None
    field: Optional[str] = None
    constant_id: Optional[str] = None
    template: Optional[str] = None
    section: Optional[str] = None
    evidence_level: Optional[EvidenceLevel] = None


class EvidenceChainStep(BaseModel):
    step: int
    description: str
    node_id: str
    relationship_id: str
    evidence: str
    relevance_level: Optional[str] = None


class EvidenceSection(BaseModel):
    chain: List[EvidenceChainStep] = []
    summary: Optional[str] = None
    total_steps: int = 0
    highest_evidence_level: Optional[str] = None


class CitationSection(BaseModel):
    citations: List[dict] = []
    total_citations: int = 0
    engine_output_citations: int = 0
    kg_node_citations: int = 0
    evidence_chain_citations: int = 0


class SystemPrompt(BaseModel):
    role: str = "system"
    content: str
    version: str = "v1.0"
    forbidden_actions: List[str] = [
        "NEVER calculate any astrological value",
        "NEVER predict values not in final_output",
        "NEVER override deterministic engine outputs",
        "NEVER speculate beyond provided deterministic outputs",
        "NEVER use external knowledge (Wikipedia, ephemeris, etc.)",
        "NEVER modify final_output values",
        "NEVER call external APIs during explanation",
        "NEVER speculate beyond provided deterministic outputs"
    ]
    required_format: str = "JSON with citations array"


class UserPrompt(BaseModel):
    role: str = "user"
    content: str
    grounding_package_hash: str
    question: str
    routed_domain: Optional[str] = None


class EvidenceSection(BaseModel):
    chain: List[dict] = []
    total_steps: int = 0
    highest_evidence_level: Optional[str] = None
    summary: Optional[str] = None


class CitationSection(BaseModel):
    citations: List[dict] = []
    total_citations: int = 0
    engine_output_citations: int = 0
    kg_node_citations: int = 0
    evidence_chain_citations: int = 0
    by_type: Dict[str, int] = {}


class Metadata(BaseModel):
    grounding_package_hash: str
    prompt_version: str = "v1.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    prompt_version: str = "v1.0"
    system_prompt_version: str = "v1.0"
    user_prompt_version: str = "v1.0"
    grounding_package_hash: str
    evidence_chain_hash: Optional[str] = None
    kg_version: str
    final_output_hash: str
    deterministic_replay_key: str


class SystemPrompt(BaseModel):
    role: str = "system"
    content: str
    version: str = "v1.0"
    forbidden_actions: List[str] = [
        "NEVER calculate any astrological value",
        "NEVER predict values not in final_output",
        "NEVER override deterministic engine outputs",
        "NEVER speculate beyond provided deterministic outputs",
        "NEVER use external knowledge (Wikipedia, ephemeris, etc.)",
        "NEVER modify final_output values",
        "NEVER call external APIs during explanation",
        "NEVER speculate beyond provided deterministic outputs"
    ]
    required_format: str = "JSON with citations array"


class UserPrompt(BaseModel):
    role: str = "user"
    content: str
    grounding_package_hash: str
    question: str
    routed_domain: Optional[str] = None


class EvidenceSection(BaseModel):
    chain: List[dict] = []
    total_steps: int = 0
    highest_evidence_level: Optional[str] = None
    summary: Optional[str] = None


class CitationSection(BaseModel):
    citations: List[dict] = []
    total_citations: int = 0
    engine_output_citations: int = 0
    kg_node_citations: int = 0
    evidence_chain_citations: int = 0
    by_type: Dict[str, int] = {}


class PromptPackage(BaseModel):
    system_prompt: SystemPrompt
    user_prompt: UserPrompt
    evidence_section: EvidenceSection
    citation_section: CitationSection
    metadata: dict = {}
    metadata_obj: Optional[dict] = None
    system_prompt_obj: Optional[dict] = None
    user_prompt_obj: Optional[dict] = None
    evidence_section_obj: Optional[dict] = None
    citation_section_obj: Optional[dict] = None
    metadata_obj: Optional[dict] = None


class GroundingPackage(BaseModel):
    """Input: The GroundingPackage from GM-012D.2"""
    chart_context: dict
    question_context: dict
    engine_outputs: dict
    evidence_chain: list
    knowledge_graph_refs: list
    formula_references: list
    probability_references: dict
    citation_package: dict
    metadata: dict


class PromptPackage(BaseModel):
    system_prompt: str
    user_prompt: str
    evidence_section: dict
    citation_section: dict
    metadata: dict
    system_prompt_obj: dict = {}
    user_prompt_obj: dict = {}
    evidence_section_obj: dict = {}
    citation_section_obj: dict = {}
    metadata_obj: dict = {}