import json
import os
import uuid
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from app.core.logging import log


from app.core.paths import get_app_data_dir
DATA_DIR = get_app_data_dir()
DATA_FILE = DATA_DIR / "knowledge_graph.json"

_lock = threading.Lock()


def _now() -> str:
    return datetime.utcnow().isoformat()

def _uid() -> str:
    return str(uuid.uuid4())


class KnowledgeStore:
    def __init__(self, file_path: Optional[str] = None):
        self._path = Path(file_path) if file_path else DATA_FILE
        with _lock:
            self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self._path.exists():
            return {"nodes": [], "relationships": [], "version": 1}
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            log.warning("Could not load knowledge_graph.json; starting fresh")
            return {"nodes": [], "relationships": [], "version": 1}

    def _save(self) -> None:
        self._data["version"] = self._data.get("version", 1) + 1
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(self._data, indent=2, ensure_ascii=False), encoding="utf-8")

    @property
    def version(self) -> int:
        return self._data.get("version", 1)

    # ── Node CRUD ──────────────────────────────────────────────────────────────

    def list_nodes(
        self,
        node_type: Optional[str] = None,
        domain: Optional[str] = None,
        source: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        nodes = self._data.get("nodes", [])
        if node_type:
            nodes = [n for n in nodes if n.get("type") == node_type]
        if domain:
            nodes = [n for n in nodes if n.get("domain") == domain]
        if source:
            nodes = [n for n in nodes if n.get("source") == source]
        return nodes

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        for n in self._data.get("nodes", []):
            if n["id"] == node_id:
                return n
        return None

    def add_node(
        self,
        type: str,
        label: str,
        description: str = "",
        source: str = "user",
        domain: str = "general",
        properties: Optional[Dict[str, Any]] = None,
        version: int = 1,
    ) -> Dict[str, Any]:
        ts = _now()
        node = {
            "id": _uid(),
            "type": type,
            "label": label,
            "description": description,
            "source": source,
            "domain": domain,
            "properties": properties or {},
            "version": version,
            "created_at": ts,
            "updated_at": ts,
        }
        with _lock:
            self._data.setdefault("nodes", []).append(node)
            self._save()
        return node

    def update_node(self, node_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with _lock:
            nodes = self._data.get("nodes", [])
            for node in nodes:
                if node["id"] == node_id:
                    node.update({k: v for k, v in updates.items() if v is not None})
                    node["version"] = node.get("version", 1) + 1
                    node["updated_at"] = _now()
                    self._save()
                    return node
        return None

    def remove_node(self, node_id: str) -> bool:
        with _lock:
            nodes = self._data.get("nodes", [])
            rels = self._data.get("relationships", [])
            old_len = len(nodes)
            self._data["nodes"] = [n for n in nodes if n["id"] != node_id]
            self._data["relationships"] = [
                r for r in rels
                if r.get("source_node_id") != node_id and r.get("target_node_id") != node_id
            ]
            if len(self._data["nodes"]) < old_len:
                self._save()
                return True
        return False

    # ── Relationship CRUD ───────────────────────────────────────────────────────

    def list_relationships(self, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        rels = self._data.get("relationships", [])
        if rel_type:
            rels = [r for r in rels if r.get("type") == rel_type]
        return rels

    def get_relationships(self, node_id: str) -> List[Dict[str, Any]]:
        return [
            r for r in self._data.get("relationships", [])
            if r.get("source_node_id") == node_id or r.get("target_node_id") == node_id
        ]

    def add_relationship(
        self,
        type: str,
        source_node_id: str,
        target_node_id: str,
        label: str = "",
        description: str = "",
        weight: float = 1.0,
        evidence: str = "",
    ) -> Dict[str, Any]:
        rel = {
            "id": _uid(),
            "type": type,
            "source_node_id": source_node_id,
            "target_node_id": target_node_id,
            "label": label,
            "description": description,
            "weight": weight,
            "evidence": evidence,
            "created_at": _now(),
        }
        with _lock:
            self._data.setdefault("relationships", []).append(rel)
            self._save()
        return rel

    def remove_relationship(self, rel_id: str) -> bool:
        with _lock:
            rels = self._data.get("relationships", [])
            old_len = len(rels)
            self._data["relationships"] = [r for r in rels if r["id"] != rel_id]
            if len(self._data["relationships"]) < old_len:
                self._save()
                return True
        return False

    # ── Search ──────────────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        node_type: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        lower = query.lower()
        nodes = self._data.get("nodes", [])
        results = []
        for node in nodes:
            if (
                lower in node.get("label", "").lower()
                or lower in node.get("description", "").lower()
                or lower in node.get("domain", "").lower()
            ):
                if node_type and node.get("type") != node_type:
                    continue
                if domain and node.get("domain") != domain:
                    continue
                results.append(node)
        return results

    # ── Evidence Chains ─────────────────────────────────────────────────────────

    def build_evidence_chain(self, node_id: str) -> List[Dict[str, Any]]:
        nodes = {n["id"]: n for n in self._data.get("nodes", [])}
        rels = self._data.get("relationships", [])
        chain: List[Dict[str, Any]] = []
        visited: set = set()

        # Relationship types that contribute to evidence chain
        evidence_rel_types = (
            "derived_from", "depends_on", "validated_by",
            "explains", "influences", "produces", "uses", "strengthens", "weakens",
            "contains", "resolves", "activates", "centered_on", "aggregates", "produced_by"
        )

        def traverse(nid: str, step: int) -> None:
            if nid in visited or nid not in nodes:
                return
            visited.add(nid)
            node = nodes[nid]
            for rel in rels:
                if rel.get("source_node_id") != nid:
                    continue
                if rel.get("type") in evidence_rel_types:
                    target = nodes.get(rel.get("target_node_id", ""))
                    chain.append({
                        "step": step,
                        "description": f"{node.get('label', '')} {rel.get('label', rel.get('type', ''))} {target.get('label', 'unknown') if target else 'unknown'}",
                        "node_id": nid,
                        "relationship_id": rel.get("id", ""),
                        "evidence": rel.get("evidence", "") or rel.get("description", ""),
                    })
                    traverse(rel.get("target_node_id", ""), step + 1)

        traverse(node_id, 1)
        return sorted(chain, key=lambda s: s["step"])

    # ── Cross References ────────────────────────────────────────────────────────

    def get_cross_references(self, node_id: str) -> List[Dict[str, Any]]:
        nodes = {n["id"]: n for n in self._data.get("nodes", [])}
        rels = self._data.get("relationships", [])
        results: List[Dict[str, Any]] = []
        node = nodes.get(node_id)
        if not node:
            return results
        for rel in rels:
            other_id = None
            if rel.get("source_node_id") == node_id:
                other_id = rel.get("target_node_id")
            elif rel.get("target_node_id") == node_id:
                other_id = rel.get("source_node_id")
            else:
                continue
            other_node = nodes.get(other_id)
            if not other_node:
                continue
            w = float(rel.get("weight", 0))
            relevance = "direct" if w >= 0.8 else "indirect" if w >= 0.5 else "contextual"
            results.append({
                "node": node,
                "relationship": rel,
                "related_node": other_node,
                "relevance": relevance,
            })
        return results

    # ── Domain Insights ─────────────────────────────────────────────────────────

    def get_domain_insights(self, domain: str) -> Dict[str, Any]:
        all_nodes = self._data.get("nodes", [])
        all_rels = self._data.get("relationships", [])
        domain_nodes = [n for n in all_nodes if n.get("domain") == domain]
        domain_node_ids = {n["id"] for n in domain_nodes}
        domain_rels = [
            r for r in all_rels
            if r.get("source_node_id") in domain_node_ids or r.get("target_node_id") in domain_node_ids
        ]
        key_concepts = [n["label"] for n in domain_nodes[:5]]
        total_domains = len({n.get("domain") for n in all_nodes if n.get("domain")})
        coverage = len(domain_nodes) / max(len(all_nodes), 1)
        return {
            "domain": domain,
            "node_count": len(domain_nodes),
            "relationship_count": len(domain_rels),
            "key_concepts": key_concepts,
            "coverage_score": round(coverage, 3),
        }

    def list_all_domain_insights(self) -> List[Dict[str, Any]]:
        all_nodes = self._data.get("nodes", [])
        domains = sorted({n["domain"] for n in all_nodes if n.get("domain")})
        return [self.get_domain_insights(d) for d in domains]

    # ── Integrity ───────────────────────────────────────────────────────────────

    def validate_integrity(self) -> Dict[str, Any]:
        nodes = self._data.get("nodes", [])
        rels = self._data.get("relationships", [])
        node_ids = {n["id"] for n in nodes}
        issues: List[str] = []
        for rel in rels:
            src = rel.get("source_node_id", "")
            tgt = rel.get("target_node_id", "")
            if src and src not in node_ids:
                issues.append(f"Relationship {rel.get('id', '?')} references missing source node {src}")
            if tgt and tgt not in node_ids:
                issues.append(f"Relationship {rel.get('id', '?')} references missing target node {tgt}")
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "node_count": len(nodes),
            "relationship_count": len(rels),
            "checked_at": _now(),
        }

    # ── Computed Fields ──────────────────────────────────────────────────────────

    def get_node_evidence(self, node_id: str) -> Dict[str, Any]:
        """Compute evidence summary for a node based on its relationships and type."""
        node = self.get_node(node_id, enrich=False)
        if not node:
            return {"summary": "Node not found", "level": "L10", "confidence": 10, "chain": []}
        
        chain = self.build_evidence_chain(node_id)
        highest_level = "L10"
        confidence = 10
        
        # Determine highest evidence level from chain
        level_map = {
            "depends_on": "L3",  # Calibration
            "derived_from": "L2",  # Formula
            "validated_by": "L1",  # Canonical Rule
            "explains": "L4",  # Engine Output
            "influences": "L4",  # Engine Output
            "produces": "L4",  # Engine Output
        }
        
        for step in chain:
            # Find the relationship type for this step
            for rel in self._data.get("relationships", []):
                if rel.get("id") == step.get("relationship_id"):
                    rel_type = rel.get("type", "")
                    if rel_type in level_map:
                        level = level_map[rel_type]
                        if level > highest_level:
                            highest_level = level
        
        # Convert level to confidence
        level_confidence = {"L1": 100, "L2": 90, "L3": 80, "L4": 70, "L5": 60, "L6": 50, "L7": 40, "L8": 30, "L9": 20, "L10": 10}
        confidence = level_confidence.get(highest_level, 10)
        
        return {
            "summary": f"Evidence chain: {len(chain)} step(s)" if chain else "No evidence chain",
            "level": highest_level,
            "confidence": confidence,
            "source": node.get("source", "unknown"),
            "revision": f"v{node.get('version', 1)}",
            "traceability": f"{node.get('type', 'unknown')} → {chain[0]['description'] if chain else 'terminal'}",
            "chain": chain[:5],  # Limit for display
        }

    def get_node_references(self, node_id: str) -> List[Dict[str, Any]]:
        """Get cross-references for a node."""
        refs = self.get_cross_references(node_id)
        return [
            {
                "node_id": r["related_node"]["id"],
                "label": r["related_node"]["label"],
                "type": r["related_node"]["type"],
                "relationship": r["relationship"]["type"],
                "relevance": r["relevance"],
            }
            for r in refs
        ]

    def get_node_relationships(self, node_id: str) -> Dict[str, int]:
        """Get relationship counts by type for a node."""
        rels = self.get_relationships(node_id)
        counts: Dict[str, int] = {}
        for rel in rels:
            rel_type = rel.get("type", "unknown")
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts

    # ── Runtime Computed Relationships (GM-012A Governance) ──────────────────────

    def get_node_uses(self, node_id: str) -> List[Dict[str, Any]]:
        """Engine → Formula: Engine uses formula (from engine imports/registry)."""
        node = self.get_node(node_id, enrich=False)
        if not node or node.get("type") != "concept" or "engine_id" not in node.get("properties", {}):
            return []
        engine_id = node["properties"]["engine_id"]
        # Engine-Formula mapping from formula registry
        engine_formula_map = {
            "UniversalMandaliEngine": ["MGC-01", "MGC-02", "MGC-03", "MGC-04", "MGC-05", "MGC-06", "MGC-07", "TMR-01", "TMR-02", "TMR-03", "TMR-04", "TMR-05"],
            "TransitEngine": ["TRN-HA-001", "TRN-BV-001", "TRN-PA-001", "TRN-DS-001", "TRN-VD-001"],
            "PlanetStrengthEngine": ["PLN-DG-001", "PLN-HP-001"],
            "NatalPromiseEngine": ["NPR-01", "NPR-02", "NPR-03", "NPR-04", "NPR-05", "NPR-06", "NPR-07", "NPR-08"],
            "MasterProbabilityEngine": ["PRB-AG-001"],
            "YogaEngine": ["YOG-DT-001"],
            "DashaEngine": ["DSH-PR-001"],
            "LifetimeCycleProjector": ["LCP-01", "LCP-02", "LCP-03", "LCP-04", "LCP-05", "LCP-06", "LCP-07", "LCP-08", "LCP-09", "LCP-10"],
        }
        formula_ids = engine_formula_map.get(engine_id, [])
        results = []
        for fid in formula_ids:
            formula_node = None
            for n in self._data.get("nodes", []):
                if n.get("type") == "formula" and n.get("properties", {}).get("formula_id") == fid:
                    formula_node = n
                    break
            if formula_node:
                results.append({
                    "node_id": formula_node["id"],
                    "label": formula_node["label"],
                    "type": "formula",
                    "relationship": "uses",
                    "relevance": "direct",
                })
        return results

    def get_node_produces(self, node_id: str) -> List[Dict[str, Any]]:
        """Engine → Node: Engine produces node (from node.source field)."""
        results = []
        for n in self._data.get("nodes", []):
            if n.get("source") == "engine":
                # Check if this engine produces the target node
                engine_concept = None
                for n2 in self._data.get("nodes", []):
                    if n2.get("type") == "concept" and n2.get("properties", {}).get("engine_id") == n["properties"].get("engine_id"):
                        engine_concept = n2
                        break
                if engine_concept and engine_concept["id"] == node_id:
                    results.append({
                        "node_id": n["id"],
                        "label": n["label"],
                        "type": n["type"],
                        "relationship": "produces",
                        "relevance": "direct",
                    })
        return results

    def get_node_affects(self, node_id: str) -> List[Dict[str, Any]]:
        """Transit → Domain: Transit affects domain (from TransitEngine output)."""
        node = self.get_node(node_id, enrich=False)
        if not node or node.get("type") != "transit":
            return []
        # Transit activation affects domains based on TransitEngine output
        # This would be computed from transit activation scores
        # For now, return empty - would need TransitEngine integration
        return []

    def get_node_weakens(self, node_id: str) -> List[Dict[str, Any]]:
        """A → B (decreases score): From seed data (weakens relationships)."""
        # Already persisted in seed data for transit quality < 0
        # Runtime computation would check transit quality matrix
        rels = self.get_relationships(node_id)
        results = []
        for rel in rels:
            if rel.get("type") == "weakens":
                target = self.get_node(rel.get("target_node_id", ""), enrich=False)
                if target:
                    results.append({
                        "node_id": target["id"],
                        "label": target["label"],
                        "type": target["type"],
                        "relationship": "weakens",
                        "relevance": "direct",
                    })
        return results

    def get_node_triggered_by(self, node_id: str) -> List[Dict[str, Any]]:
        """Event → Transit: Inverse of activates (from Gochara Mandali)."""
        results = []
        # Find all activates relationships where this node is target
        for rel in self._data.get("relationships", []):
            if rel.get("type") == "activates" and rel.get("target_node_id") == node_id:
                source = self.get_node(rel.get("source_node_id", ""), enrich=False)
                if source:
                    results.append({
                        "node_id": source["id"],
                        "label": source["label"],
                        "type": source["type"],
                        "relationship": "triggered_by",
                        "relevance": "direct",
                    })
        return results

    def get_node_used_in(self, node_id: str) -> List[Dict[str, Any]]:
        """Formula → Engine: Formula used in engine (from formula registry used_by_engine)."""
        node = self.get_node(node_id, enrich=False)
        if not node or node.get("type") != "formula":
            return []
        fid = node.get("properties", {}).get("formula_id", "")
        formula_engine_map = {
            "TRN-HA-001": "TransitEngine",
            "TRN-BV-001": "TransitEngine",
            "TRN-PA-001": "TransitEngine",
            "TRN-DS-001": "TransitEngine",
            "TRN-VD-001": "TransitEngine",
            "PLN-DG-001": "PlanetStrengthEngine",
            "PLN-HP-001": "PlanetStrengthEngine",
            "PRB-AG-001": "MasterProbabilityEngine",
            "DSH-PR-001": "DashaEngine",
            "YOG-DT-001": "YogaEngine",
        }
        engine_name = formula_engine_map.get(fid)
        if not engine_name:
            return []
        engine_concept = None
        for n in self._data.get("nodes", []):
            if n.get("type") == "concept" and n.get("properties", {}).get("engine_id") == engine_name:
                engine_concept = n
                break
        if engine_concept:
            return [{
                "node_id": engine_concept["id"],
                "label": engine_concept["label"],
                "type": "concept",
                "relationship": "used_in",
                "relevance": "direct",
            }]
        return []

    def get_node_appears_in_report(self, node_id: str) -> List[Dict[str, Any]]:
        """Node → Report: Node appears in report (from report templates)."""
        # Report templates define which node types appear in which reports
        report_templates = {
            "planet": ["Planet Strength Report", "Natal Promise Domain Scores", "Transit Report"],
            "house": ["House Strength Report", "Domain Promise Report"],
            "transit": ["Transit Report", "Gochara Mandali Advisory", "Lifetime Cycle Projection"],
            "formula": ["Formula Evaluation Report", "Subsystem Breakdown"],
            "calibration": ["Calibration Audit", "Formula Evaluation"],
            "yoga": ["Yoga Report", "Natal Promise modifiers"],
            "dasha": ["Dasha Report", "Dasha-Transit Sync", "Lifetime Cycle Projection"],
            "gochara_mandali": ["Gochara Mandali Advisory", "Mandali Activations"],
            "mandali": ["Current Mandali", "Mandali Activations", "Transit Mandali Resolution"],
            "probability": ["Master Probability Report", "Question Answer", "Consultation Report"],
            "yoga": ["Yoga Report", "Natal Promise modifiers"],
        }
        node = self.get_node(node_id, enrich=False)
        if not node:
            return []
        report_names = report_templates.get(node.get("type", ""), [])
        return [{"report_name": rn, "relationship": "appears_in_report", "relevance": "direct"} for rn in report_names]

    def get_node_asked_by_question(self, node_id: str) -> List[Dict[str, Any]]:
        """Question → Node: Question queries node (from Question Registry domain)."""
        node = self.get_node(node_id, enrich=False)
        if not node:
            return []
        # Map node type/domain to question registry
        domain_question_map = {
            "marriage": ["Q2.1", "Q2.2", "Q2.3"],
            "career": ["Q3.1", "Q3.2"],
            "wealth": ["Q4.1", "Q4.2"],
            "health": ["Q5.1", "Q5.2"],
            "children": ["Q6.1", "Q6.2"],
            "property": ["Q7.1", "Q7.2"],
            "education": ["Q8.1", "Q8.2"],
            "travel": ["Q9.1", "Q9.2"],
            "spiritual": ["Q10.1", "Q10.2"],
            "compatibility": ["Q11.1", "Q11.2"],
            "retirement": ["Q12.1", "Q12.2"],
        }
        domain = node.get("domain", "")
        question_ids = domain_question_map.get(domain, [])
        results = []
        for qid in question_ids:
            results.append({
                "question_id": qid,
                "relationship": "asked_by_question",
                "relevance": "direct",
            })
        return results

    def get_node_used_by_engine(self, node_id: str) -> List[Dict[str, Any]]:
        """Node → Engine: Node consumed by engine (from engine input schemas)."""
        node = self.get_node(node_id, enrich=False)
        if not node:
            return []
        engine_input_map = {
            "planet": ["PlanetStrengthEngine", "TransitEngine", "NatalPromiseEngine", "MasterProbabilityEngine"],
            "house": ["HouseStrengthEngine", "NatalPromiseEngine"],
            "transit": ["TransitEngine", "UniversalMandaliEngine", "LifetimeCycleProjector"],
            "formula": ["TransitEngine", "PlanetStrengthEngine", "MasterProbabilityEngine", "YogaEngine", "DashaEngine"],
            "calibration": ["PlanetStrengthEngine", "TransitEngine", "MasterProbabilityEngine"],
            "dasha": ["DashaEngine", "TransitEngine", "LifetimeCycleProjector"],
            "yoga": ["YogaEngine", "NatalPromiseEngine"],
            "gochara_mandali": ["UniversalMandaliEngine", "LifetimeCycleProjector"],
            "probability": ["QuestionEngine"],
            "yoga": ["YogaEngine", "NatalPromiseEngine"],
        }
        engines = engine_input_map.get(node.get("type", ""), [])
        results = []
        for engine_name in engines:
            engine_concept = None
            for n in self._data.get("nodes", []):
                if n.get("type") == "concept" and n.get("properties", {}).get("engine_id") == engine_name:
                    engine_concept = n
                    break
            if engine_concept:
                results.append({
                    "node_id": engine_concept["id"],
                    "label": engine_concept["label"],
                    "type": "concept",
                    "relationship": "used_by_engine",
                    "relevance": "direct",
                })
        return results

    def get_node_derived_from(self, node_id: str) -> List[Dict[str, Any]]:
        """Node → Formula: Node derived from formula (from formula registry output_node)."""
        node = self.get_node(node_id, enrich=False)
        if not node:
            return []
        # Map node types to their generating formulas
        node_formula_map = {
            "transit": ["TRN-HA-001", "TRN-BV-001", "TRN-PA-001", "TRN-DS-001", "TRN-VD-001"],
            "planet": ["PLN-DG-001", "PLN-HP-001"],
            "probability": ["PRB-AG-001"],
            "yoga": ["YOG-DT-001"],
            "dasha": ["DSH-PR-001"],
            "gochara_mandali": ["MGC-01", "MGC-02", "MGC-03", "MGC-04", "MGC-04", "MGC-05", "MGC-06", "MGC-07"],
            "mandali": ["MGC-01", "MGC-02", "MGC-03", "MGC-04", "MGC-05", "MGC-06", "MGC-07"],
            "dasha": ["DSH-PR-001"],
        }
        formula_ids = node_formula_map.get(node.get("type", ""), [])
        results = []
        for fid in formula_ids:
            formula_node = None
            for n in self._data.get("nodes", []):
                if n.get("type") == "formula" and n.get("properties", {}).get("formula_id") == fid:
                    formula_node = n
                    break
            if formula_node:
                results.append({
                    "node_id": formula_node["id"],
                    "label": formula_node["label"],
                    "type": "formula",
                    "relationship": "derived_from",
                    "relevance": "direct",
                })
        return results

    def get_node_calibrated_by(self, node_id: str) -> List[Dict[str, Any]]:
        """Formula → Calibration: Inverse of depends_on (auto-generated)."""
        node = self.get_node(node_id, enrich=False)
        if not node or node.get("type") != "formula":
            return []
        # Find all depends_on relationships from this formula to calibrations
        rels = self.get_relationships(node_id)
        results = []
        for rel in rels:
            if rel.get("type") == "depends_on":
                target = self.get_node(rel.get("target_node_id", ""), enrich=False)
                if target and target.get("type") == "calibration":
                    results.append({
                        "node_id": target["id"],
                        "label": target["label"],
                        "type": "calibration",
                        "relationship": "calibrated_by",
                        "relevance": "direct",
                    })
        return results

    def get_all_computed_relationships(self, node_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get all computed relationships for a node."""
        return {
            "uses": self.get_node_uses(node_id),
            "produces": self.get_node_produces(node_id),
            "affects": self.get_node_affects(node_id),
            "weakens": self.get_node_weakens(node_id),
            "triggered_by": self.get_node_triggered_by(node_id),
            "used_in": self.get_node_used_in(node_id),
            "appears_in_report": self.get_node_appears_in_report(node_id),
            "asked_by_question": self.get_node_asked_by_question(node_id),
            "used_by_engine": self.get_node_used_by_engine(node_id),
            "derived_from": self.get_node_derived_from(node_id),
            "calibrated_by": self.get_node_calibrated_by(node_id),
        }

    def _enrich_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Add computed fields to a node."""
        enriched = dict(node)
        enriched["evidence"] = self.get_node_evidence(node["id"])
        enriched["references"] = self.get_node_references(node["id"])
        enriched["relationships"] = self.get_node_relationships(node["id"])
        enriched["computed_relationships"] = self.get_all_computed_relationships(node["id"])
        return enriched

    # Update list_nodes and get_node to include computed fields
    def list_nodes(
        self,
        node_type: Optional[str] = None,
        domain: Optional[str] = None,
        source: Optional[str] = None,
        enrich: bool = True,
    ) -> List[Dict[str, Any]]:
        nodes = self._data.get("nodes", [])
        if node_type:
            nodes = [n for n in nodes if n.get("type") == node_type]
        if domain:
            nodes = [n for n in nodes if n.get("domain") == domain]
        if source:
            nodes = [n for n in nodes if n.get("source") == source]
        if enrich:
            nodes = [self._enrich_node(n) for n in nodes]
        return nodes

    def get_node(self, node_id: str, enrich: bool = True) -> Optional[Dict[str, Any]]:
        for n in self._data.get("nodes", []):
            if n["id"] == node_id:
                return self._enrich_node(n) if enrich else n
        return None

    # ── Seed ────────────────────────────────────────────────────────────────────

    def seed_default_data(self) -> None:
        with _lock:
            existing = self._data.get("nodes", [])
            if existing:
                return

            ts = _now()
            nodes: List[Dict[str, Any]] = []
            rels: List[Dict[str, Any]] = []

            def add_node(type: str, label: str, desc: str, source: str, domain: str, props: Optional[Dict] = None) -> str:
                nid = _uid()
                nodes.append({
                    "id": nid, "type": type, "label": label,
                    "description": desc, "source": source, "domain": domain,
                    "properties": props or {}, "version": 1,
                    "created_at": ts, "updated_at": ts,
                })
                return nid

            def add_rel(src: str, tgt: str, rtype: str, label: str, weight: float, evidence: str) -> None:
                rels.append({
                    "id": _uid(), "type": rtype, "source_node_id": src, "target_node_id": tgt,
                    "label": label, "description": label, "weight": weight,
                    "evidence": evidence, "created_at": ts,
                })

            # Planets
            planets: Dict[str, str] = {}
            planet_data = [
                ("Sun", "Soul, authority, father, government"),
                ("Moon", "Mind, emotions, mother, public"),
                ("Mars", "Energy, courage, siblings, property"),
                ("Mercury", "Intellect, communication, business"),
                ("Jupiter", "Wisdom, wealth, children, fortune"),
                ("Venus", "Love, beauty, luxury, arts"),
                ("Saturn", "Discipline, longevity, suffering, delay"),
                ("Rahu", "Obsession, foreign, unconventional"),
                ("Ketu", "Detachment, spirituality, past life"),
            ]
            for name, sig in planet_data:
                pid = add_node("planet", name, f"{name} — Planet", "engine", "general", {"significance": sig})
                planets[name] = pid

            # Houses
            house_ids: List[str] = []
            bhava_names = {
                1: "Lagna/Ascendant", 2: "Dhana", 3: "Sahaja", 4: "Sukha",
                5: "Putra", 6: "Shatru", 7: "Kalatra", 8: "Ayush", 9: "Dharma",
                10: "Karma", 11: "Labha", 12: "Vyaya",
            }
            for i in range(1, 13):
                hid = add_node("house", f"House {i}", f"Bhava — {bhava_names[i]}", "engine", "house", {"house_number": i})
                house_ids.append(hid)

            # Formulas
            formulas = [
                ("TRN-HA-001", "House Activation", "transit", "30% weight — Measures house activation from transit"),
                ("TRN-BV-001", "BAV Support", "transit", "20% weight — Ashtakavarga support evaluation"),
                ("TRN-PA-001", "Planet Activation", "transit", "20% weight — Planet activation strength"),
                ("TRN-DS-001", "Dasha Sync", "transit", "20% weight — Dasha period synchronization"),
                ("TRN-VD-001", "Vedha Layer", "transit", "10% weight — Vedha obstruction detection"),
                ("PLN-DG-001", "Dignity Score", "planet", "Evaluates planetary dignity from sign placement"),
                ("PLN-HP-001", "House Placement", "planet", "Evaluates house placement strength"),
                ("PRB-AG-001", "Probability Aggregation", "probability", "Aggregates subsystem scores"),
                ("DSH-PR-001", "Dasha Period", "dasha", "Calculates dasha period from Vimshottari"),
                ("YOG-DT-001", "Yoga Detection", "yoga", "Detects planetary combinations (yogas)"),
            ]
            formula_ids: Dict[str, str] = {}
            formula_by_domain: Dict[str, List[str]] = {}
            for fid, label, domain, desc in formulas:
                nid = add_node("formula", f"{label} ({fid})", desc, "formula", domain, {"formula_id": fid})
                formula_ids[fid] = nid
                formula_by_domain.setdefault(domain, []).append(nid)

            # Calibrations
            calibrations = [
                ("own_sign", "Own Sign", "80 — Planet in own sign: 80% strength", "planet"),
                ("friendly", "Friendly Sign", "60 — Planet in friendly sign: 60% strength", "planet"),
                ("neutral", "Neutral Sign", "50 — Planet in neutral sign: 50% strength", "planet"),
                ("enemy", "Enemy Sign", "40 — Planet in enemy sign: 40% strength", "planet"),
                ("debilitated", "Debilitated", "20 — Planet debilitated: 20% strength", "planet"),
            ]
            cal_ids: List[str] = []
            for cid, label, desc, domain in calibrations:
                nid = add_node("calibration", label, desc, "calibration", domain, {"constant_id": cid})
                cal_ids.append(nid)

            # Transit nodes
            transit_ids: Dict[str, str] = {}
            transit_ids["activation"] = add_node("transit", "Transit Activation", "Overall transit activation score (0-100)", "engine", "transit", {"has_subsystems": True})
            transit_ids["sadesati"] = add_node("transit", "Sadesati", "Saturn transit over Moon sign — 7.5 year period", "engine", "transit", {"planet": "Saturn", "duration": "7.5 years"})
            transit_ids["ashtam"] = add_node("transit", "Ashtam Shani", "Saturn transit in 8th house from Moon", "engine", "transit", {"planet": "Saturn"})
            transit_ids["jupiter_return"] = add_node("transit", "Jupiter Return", "Jupiter returns to natal position every ~12 years", "engine", "transit", {"planet": "Jupiter", "period": 12})

            # Dasha periods
            dasha_periods = [
                "Ketu Mahadasha", "Venus Mahadasha", "Sun Mahadasha", "Moon Mahadasha",
                "Mars Mahadasha", "Rahu Mahadasha", "Jupiter Mahadasha", "Saturn Mahadasha", "Mercury Mahadasha",
            ]
            dasha_ids: List[str] = []
            for dp in dasha_periods:
                nid = add_node("dasha", dp, "Vimshottari Mahadasha period", "engine", "dasha", {"system": "Vimshottari"})
                dasha_ids.append(nid)

            # Governance nodes
            gov_ids: Dict[str, str] = {}
            gov_ids["ai"] = add_node("governance", "AI Governance (AP-002)", "AI assistance rules and boundaries", "governance", "governance", {"document_id": "AP-002"})
            gov_ids["system"] = add_node("governance", "System Governance (AP-003)", "Platform-wide governance rules", "governance", "governance", {"document_id": "AP-003"})
            gov_ids["freeze"] = add_node("governance", "GM-007 Freeze", "Permanent freeze of deterministic engines", "governance", "governance", {"milestone": "GM-007"})

            # Relationships
            # Formula → Calibration dependencies
            for fid in formula_ids.values():
                for cid in cal_ids:
                    add_rel(fid, cid, "depends_on", f"Formula depends on calibration constant", 0.8, "Formula-calibration dependency")

            # Transit formulas → Transit Activation
            for fid in formula_by_domain.get("transit", []):
                add_rel(fid, transit_ids["activation"], "explains", f"Formula contributes to transit activation", 0.9, "Transit subsystem")

            # Dignity Score → Planets
            dignity_id = formula_ids.get("PLN-DG-001", "")
            if dignity_id:
                for pid in planets.values():
                    add_rel(dignity_id, pid, "influences", f"Dignity score applies to planet", 0.7, "Planet strength")

            # Houses → Planets
            for hid in house_ids:
                for pid in planets.values():
                    add_rel(hid, pid, "references", f"Planet may occupy house", 0.5, "House-planet relationship")

            # Calibrations → Planet Activation
            planet_act_id = formula_ids.get("TRN-PA-001", "")
            if planet_act_id:
                for cid in cal_ids:
                    add_rel(cid, planet_act_id, "influences", f"Calibration calibrates planet strength", 0.6, "Calibration influence")

            # Governance hierarchy
            if gov_ids.get("system") and gov_ids.get("ai"):
                add_rel(gov_ids["system"], gov_ids["ai"], "supersedes", "System Governance is supreme", 1.0, "Governance hierarchy")
            if gov_ids.get("freeze") and gov_ids.get("system"):
                add_rel(gov_ids["freeze"], gov_ids["system"], "validated_by", "Freeze enforced by governance", 1.0, "Freeze governance")

            # ── Gochara Mandali & Mandali Nodes (Capability 7.1-7.7) ──────────────────
            gochara_id = add_node(
                "gochara_mandali",
                "Gochara Mandali (Current)",
                "Moon-centered 12-mandali grid resolving current transit positions to mandali numbers for precise gochara analysis",
                "engine",
                "transit",
                {
                    "mandali_number": 0,
                    "center_nakshatra": "Krittika",
                    "center_pada": 1,
                    "reference_moon_nakshatra": "Krittika",
                    "reference_moon_pada": 1,
                    "current_transit_mandali": {}
                }
            )

            # 12 Mandali nodes (1-12)
            mandali_ids: List[str] = []
            nakshatra_centers = [
                (1, "Krittika", 1, "Mesha"),      (2, "Rohini", 2, "Vrishabha"),
                (3, "Mrigashira", 3, "Mithuna"),  (4, "Ardra", 4, "Mithuna"),
                (5, "Punarvasu", 1, "Karka"),     (6, "Pushya", 2, "Karka"),
                (7, "Ashlesha", 3, "Karka"),      (8, "Magha", 4, "Simha"),
                (9, "Purva Phalguni", 1, "Simha"), (10, "Uttara Phalguni", 2, "Kanya"),
                (11, "Hasta", 3, "Kanya"),        (12, "Chitra", 4, "Tula"),
            ]
            for num, center_nak, center_pada, rasi in nakshatra_centers:
                # Calculate 9 padas for this mandali (center pada ±4)
                start_pada = (center_pada - 5) if center_pada > 4 else (center_pada + 103)
                padas = [(start_pada + i - 1) % 108 + 1 for i in range(9)]
                mid = add_node(
                    "mandali",
                    f"Mandali {num}",
                    f"Center={center_nak} Pada {center_pada}, Rasi={rasi}. Contains 9 padas from {padas[0]} to {padas[-1]}",
                    "engine",
                    "transit",
                    {
                        "number": num,
                        "center_pada": center_pada + (num - 1) * 9,  # approximate absolute pada
                        "center_nakshatra": center_nak,
                        "center_pada_num": center_pada,
                        "rasi_name": rasi,
                        "padas": padas,
                        "pada_details": [{"pada": p, "nakshatra": center_nak} for p in padas]
                    }
                )
                mandali_ids.append(mid)

            # Gochara Mandali relationships
            # Moon → Gochara Mandali (centered_on)
            moon_id = planets.get("Moon")
            if moon_id:
                add_rel(moon_id, gochara_id, "centered_on", "Moon nakshatra/pada centers the mandali", 1.0, "Moon-centered frame")

            # Gochara Mandali → Mandali 1-12 (contains)
            for mid in mandali_ids:
                add_rel(gochara_id, mid, "contains", "Gochara Mandali contains this mandali", 0.9, "Mandali grid")

            # Gochara Mandali → Transit nodes (resolves)
            for tid in transit_ids.values():
                add_rel(gochara_id, tid, "resolves", "Mandali resolves transit to mandali number", 0.8, "Transit resolution")

            # Gochara Mandali → Sadesati/Ashtam/Elinati (activates)
            for key in ("sadesati", "ashtam"):
                if key in transit_ids:
                    add_rel(gochara_id, transit_ids[key], "activates", "Mandali activates this transit cycle", 0.7, "Cycle activation")

            # Universal Mandali Engine → Gochara Mandali (produces)
            # We'll add this after engine node creation conceptually

            # ── Yoga Nodes ─────────────────────────────────────────────────────────
            yoga_data = [
                ("Gaja Kesari Yoga", "Jupiter in Kendra from Moon. Bestows wisdom, wealth, royal status.", ["Jupiter", "Moon"], [1, 4, 7, 10]),
                ("Raja Yoga", "Lords of Kendra and Trikona in mutual association.", ["Jupiter", "Venus", "Mercury"], [1, 4, 7, 10, 5, 9]),
                ("Dhana Yoga", "Lords of 2nd and 11th houses in conjunction or mutual aspect.", ["Jupiter", "Venus"], [2, 11]),
                ("Moksha Yoga", "Ketu in 12th or 4th from Moon; spiritual liberation indicators.", ["Ketu", "Moon"], [4, 12]),
                ("Ruchaka Yoga", "Mars in own sign in Kendra. Bestows courage, leadership, military success.", ["Mars"], [1, 4, 7, 10]),
            ]
            yoga_ids: List[str] = []
            for yname, ydesc, yplanets, yhouses in yoga_data:
                yid = add_node("yoga", yname, ydesc, "engine", "yoga", {
                    "yoga_name": yname,
                    "classical_type": "raja" if "Raja" in yname else "dhana" if "Dhana" in yname else "moksha" if "Moksha" in yname else "pancha_mahapurusha",
                    "strength": 80,
                    "planets_involved": yplanets,
                    "houses_involved": yhouses,
                })
                yoga_ids.append(yid)
                # Yoga detected by Yoga Engine (produces relationship)
                add_rel(yid, formula_ids.get("YOG-DT-001", ""), "produced_by", "Yoga detected by Yoga Detection formula", 0.9, "Yoga engine output")
                # Yoga modifies domains (strengthens/weakens)
                if "Dhana" in yname:
                    add_rel(yid, transit_ids["activation"], "strengthens", "Dhana Yoga strengthens wealth transit", 0.7, "Yoga modifier")
                if "Moksha" in yname:
                    add_rel(yid, transit_ids["activation"], "strengthens", "Moksha Yoga strengthens spiritual transit", 0.7, "Yoga modifier")

            # ── Probability Node (Master Probability) ────────────────────────────────
            prob_id = add_node(
                "probability",
                "Master Probability (Marriage: 61/100)",
                "Marriage: 61/100 (MODERATE). Natal Promise: 45, Transit: 78, Dasha: 65",
                "engine",
                "probability",
                {
                    "final_score": 61,
                    "grade": "MODERATE",
                    "breakdown": {"natal_promise": 45, "transit": 78, "dasha": 65},
                    "weights": {"natal": 0.4, "transit": 0.05, "dasha": 0.1, "planet": 0.15, "house": 0.1, "rasi": 0.1, "varga": 0.1},
                    "stub_factors": ["Saturn MD", "Jupiter AD", "Jupiter transit H9"],
                }
            )
            # Probability aggregates from subsystems (aggregates relationships)
            add_rel(prob_id, formula_ids.get("PRB-AG-001", ""), "aggregates", "Probability aggregated by formula", 1.0, "Master probability")

            # ── Engine → Node relationships (produces) ──────────────────────────────
            # Conceptual: UniversalMandaliEngine produces Gochara Mandali
            # We represent engines as implicit producers
            engine_nodes = {
                "UniversalMandaliEngine": "Universal Mandali Engine",
                "TransitEngine": "Transit Engine",
                "PlanetStrengthEngine": "Planet Strength Engine",
                "NatalPromiseEngine": "Natal Promise Engine",
                "MasterProbabilityEngine": "Master Probability Engine",
                "YogaEngine": "Yoga Engine",
                "DashaEngine": "Dasha Engine",
                "LifetimeCycleProjector": "Lifetime Cycle Projector",
            }
            # Add engine as concept nodes for traceability
            for eid, elabel in engine_nodes.items():
                add_node("concept", elabel, f"Deterministic engine: {elabel}", "engine", "engine", {"engine_id": eid})

            # Engine → Node (produces)
            # UniversalMandaliEngine → Gochara Mandali
            # TransitEngine → Transit Activation
            # PlanetStrengthEngine → Planet nodes
            # MasterProbabilityEngine → Probability node
            # YogaEngine → Yoga nodes
            # DashaEngine → Dasha nodes
            # LifetimeCycleProjector → Transit cycles

            self._data["nodes"] = nodes
            self._data["relationships"] = rels
            self._data["version"] = 1
            self._save()