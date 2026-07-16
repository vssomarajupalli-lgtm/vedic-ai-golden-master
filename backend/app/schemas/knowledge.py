from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class KnowledgeNodeCreate(BaseModel):
    type: str = Field(..., description="Node type: planet, house, formula, etc.")
    label: str = Field(..., description="Human-readable label")
    description: str = Field(default="", description="Node description")
    source: str = Field(default="user", description="Data source")
    domain: str = Field(default="general", description="Knowledge domain")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Node properties")
    version: int = Field(default=1, description="Node version")


class KnowledgeNodeUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    version: Optional[int] = None


class KnowledgeRelationshipCreate(BaseModel):
    type: str = Field(..., description="Relationship type")
    source_node_id: str = Field(..., description="Source node ID")
    target_node_id: str = Field(..., description="Target node ID")
    label: str = Field(default="", description="Relationship label")
    description: str = Field(default="", description="Relationship description")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Relationship weight")
    evidence: str = Field(default="", description="Supporting evidence")


class KnowledgeNode(BaseModel):
    id: str
    type: str
    label: str
    description: str
    source: str
    domain: str
    properties: Dict[str, Any]
    version: int
    created_at: str
    updated_at: str


class KnowledgeRelationship(BaseModel):
    id: str
    type: str
    source_node_id: str
    target_node_id: str
    label: str
    description: str
    weight: float
    evidence: str
    created_at: str


class KnowledgeGraphState(BaseModel):
    nodes: List[KnowledgeNode] = Field(default_factory=list)
    relationships: List[KnowledgeRelationship] = Field(default_factory=list)
    version: int = Field(default=1)
    node_count: int = Field(default=0)
    relationship_count: int = Field(default=0)


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    node_type: Optional[str] = Field(None, description="Filter by node type")
    domain: Optional[str] = Field(None, description="Filter by domain")
    limit: int = Field(default=50, ge=1, le=200)


class KnowledgeSearchResponse(BaseModel):
    nodes: List[KnowledgeNode]
    total: int


class KnowledgeEvidenceChainStep(BaseModel):
    step: int
    description: str
    node_id: str
    relationship_id: str
    evidence: str


class KnowledgeEvidenceChain(BaseModel):
    formula_id: str
    chain: List[KnowledgeEvidenceChainStep]


class KnowledgeCrossReference(BaseModel):
    node: KnowledgeNode
    relationship: KnowledgeRelationship
    related_node: KnowledgeNode
    relevance: str


class KnowledgeInsight(BaseModel):
    domain: str
    node_count: int
    relationship_count: int
    key_concepts: List[str]
    coverage_score: float


class KnowledgeIntegrityReport(BaseModel):
    valid: bool
    issues: List[str] = Field(default_factory=list)
    node_count: int
    relationship_count: int
    checked_at: str