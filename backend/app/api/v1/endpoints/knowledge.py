from fastapi import APIRouter, HTTPException, Query
from typing import Any, Dict, List, Optional
import traceback
import uuid
from datetime import datetime

from app.core.logging import log
from app.core.knowledge_store import KnowledgeStore
from app.schemas.knowledge import (
    KnowledgeNodeCreate, KnowledgeNodeUpdate, KnowledgeRelationshipCreate,
    KnowledgeNode, KnowledgeRelationship, KnowledgeGraphState,
    KnowledgeSearchRequest, KnowledgeSearchResponse,
    KnowledgeEvidenceChain, KnowledgeEvidenceChainStep,
    KnowledgeCrossReference, KnowledgeInsight, KnowledgeIntegrityReport,
)

router = APIRouter()

store = KnowledgeStore()


def _now() -> str:
    return datetime.utcnow().isoformat()


def _uid() -> str:
    return str(uuid.uuid4())


# ── Node CRUD ────────────────────────────────────────────────────────────────

@router.get("/nodes", response_model=List[KnowledgeNode])
def list_nodes(
    node_type: Optional[str] = Query(None, description="Filter by node type"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    source: Optional[str] = Query(None, description="Filter by source"),
) -> Any:
    try:
        return store.list_nodes(node_type=node_type, domain=domain, source=source)
    except Exception as e:
        log.error(f"Error listing nodes: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nodes/{node_id}", response_model=KnowledgeNode)
def get_node(node_id: str) -> Any:
    try:
        node = store.get_node(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        return node
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting node: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nodes", response_model=KnowledgeNode, status_code=201)
def create_node(body: KnowledgeNodeCreate) -> Any:
    try:
        node = store.add_node(
            type=body.type,
            label=body.label,
            description=body.description,
            source=body.source,
            domain=body.domain,
            properties=body.properties,
            version=body.version,
        )
        return node
    except Exception as e:
        log.error(f"Error creating node: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/nodes/{node_id}", response_model=KnowledgeNode)
def update_node(node_id: str, body: KnowledgeNodeUpdate) -> Any:
    try:
        node = store.update_node(node_id, body.dict(exclude_none=True))
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        return node
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error updating node: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/nodes/{node_id}")
def delete_node(node_id: str) -> Any:
    try:
        removed = store.remove_node(node_id)
        if not removed:
            raise HTTPException(status_code=404, detail="Node not found")
        return {"status": "deleted", "node_id": node_id}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting node: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Relationship CRUD ────────────────────────────────────────────────────────

@router.get("/relationships", response_model=List[KnowledgeRelationship])
def list_relationships(
    node_id: Optional[str] = Query(None, description="Filter by node ID"),
    rel_type: Optional[str] = Query(None, description="Filter by relationship type"),
) -> Any:
    try:
        if node_id:
            return store.get_relationships(node_id)
        return store.list_relationships(rel_type=rel_type)
    except Exception as e:
        log.error(f"Error listing relationships: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/relationships", response_model=KnowledgeRelationship, status_code=201)
def create_relationship(body: KnowledgeRelationshipCreate) -> Any:
    try:
        rel = store.add_relationship(
            type=body.type,
            source_node_id=body.source_node_id,
            target_node_id=body.target_node_id,
            label=body.label or body.description,
            description=body.description or body.label,
            weight=body.weight,
            evidence=body.evidence,
        )
        return rel
    except Exception as e:
        log.error(f"Error creating relationship: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/relationships/{rel_id}")
def delete_relationship(rel_id: str) -> Any:
    try:
        removed = store.remove_relationship(rel_id)
        if not removed:
            raise HTTPException(status_code=404, detail="Relationship not found")
        return {"status": "deleted", "relationship_id": rel_id}
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting relationship: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Search ───────────────────────────────────────────────────────────────────

@router.post("/search", response_model=KnowledgeSearchResponse)
def search_knowledge(body: KnowledgeSearchRequest) -> Any:
    try:
        results = store.search(body.query, node_type=body.node_type, domain=body.domain)
        return KnowledgeSearchResponse(
            nodes=results[:body.limit],
            total=len(results),
        )
    except Exception as e:
        log.error(f"Error searching: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Evidence Chains ──────────────────────────────────────────────────────────

@router.get("/evidence-chain/{node_id}", response_model=KnowledgeEvidenceChain)
def get_evidence_chain(node_id: str) -> Any:
    try:
        node = store.get_node(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        chain = store.build_evidence_chain(node_id)
        return KnowledgeEvidenceChain(formula_id=node_id, chain=chain)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error building evidence chain: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Cross References ─────────────────────────────────────────────────────────

@router.get("/cross-references/{node_id}", response_model=List[KnowledgeCrossReference])
def get_cross_references(node_id: str) -> Any:
    try:
        return store.get_cross_references(node_id)
    except Exception as e:
        log.error(f"Error getting cross references: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Domain Insights ──────────────────────────────────────────────────────────

@router.get("/insights/{domain}", response_model=KnowledgeInsight)
def get_domain_insights(domain: str) -> Any:
    try:
        return store.get_domain_insights(domain)
    except Exception as e:
        log.error(f"Error getting domain insights: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights", response_model=List[KnowledgeInsight])
def list_domain_insights() -> Any:
    try:
        return store.list_all_domain_insights()
    except Exception as e:
        log.error(f"Error listing domain insights: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Integrity ────────────────────────────────────────────────────────────────

@router.get("/integrity", response_model=KnowledgeIntegrityReport)
def get_integrity_report() -> Any:
    try:
        return store.validate_integrity()
    except Exception as e:
        log.error(f"Error validating integrity: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ── State / Import / Export ──────────────────────────────────────────────────

@router.get("/state", response_model=KnowledgeGraphState)
def get_state() -> Any:
    try:
        nodes = store.list_nodes()
        rels = store.list_relationships()
        return KnowledgeGraphState(
            nodes=nodes,
            relationships=rels,
            version=store.version,
            node_count=len(nodes),
            relationship_count=len(rels),
        )
    except Exception as e:
        log.error(f"Error getting state: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/seed")
def seed_knowledge_graph() -> Any:
    try:
        if len(store.list_nodes()) > 0:
            return {"status": "skipped", "message": "Knowledge graph already seeded"}
        store.seed_default_data()
        return {
            "status": "seeded",
            "node_count": len(store.list_nodes()),
            "relationship_count": len(store.list_relationships()),
        }
    except Exception as e:
        log.error(f"Error seeding: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))