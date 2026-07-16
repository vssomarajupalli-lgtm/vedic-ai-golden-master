import json
import os
import uuid
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from app.core.logging import log


DATA_DIR = Path(__file__).resolve().parent.parent / "database"
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

        def traverse(nid: str, step: int) -> None:
            if nid in visited or nid not in nodes:
                return
            visited.add(nid)
            node = nodes[nid]
            for rel in rels:
                if rel.get("source_node_id") != nid:
                    continue
                if rel.get("type") in ("derived_from", "depends_on", "validated_by"):
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

            self._data["nodes"] = nodes
            self._data["relationships"] = rels
            self._data["version"] = 1
            self._save()