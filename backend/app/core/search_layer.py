from typing import List, Dict, Any, Optional
from app.core.registry_loader import QuestionRegistryLoader

class SearchLayer:
    """
    SearchLayer acts as the NLP Free-Text fallback and search engine.
    It maps user text queries to deterministic domains and child Question IDs.
    """
    def __init__(self, loader: Optional[QuestionRegistryLoader] = None):
        self.loader = loader or QuestionRegistryLoader()
        
        # We attempt to safely load registry data
        try:
            self.registry_data = self.loader.load_registry()
        except Exception:
            self.registry_data = []

        # 1. Search Dictionary Layer
        self.domain_aliases = {
            # Marriage Synonyms & Typos -> Domain 7
            "marriage": 7,
            "marrage": 7,
            "marraige": 7,
            "wife": 7,
            "husband": 7,
            "spouse": 7,
            "wedding": 7,
            "divorce": 7,
            
            # Career Synonyms & Typos -> Domain 10
            "career": 10,
            "job": 10,
            "profession": 10,
            "employment": 10,
            "work": 10,
            "promotion": 10,
            "business": 10,
            
            # Wealth Synonyms & Typos -> Domain 2
            "wealth": 2,
            "money": 2,
            "income": 2,
            "finance": 2,
            "savings": 2,
            "rich": 2,
            "financial": 2
        }

    def resolve(self, query: str) -> Dict[str, Any]:
        """
        Resolves a free-text string to matching Question IDs.
        Returns a dictionary indicating success or safe error states.
        """
        if not query or not isinstance(query, str) or not query.strip():
            return {
                "status": "error",
                "error_type": "empty_search",
                "message": "Search query cannot be empty."
            }

        # Basic normalization
        normalized_query = query.lower().strip()
        
        # Tokenize by spaces and strip punctuation to match dictionary
        tokens = "".join([c if c.isalnum() or c.isspace() else " " for c in normalized_query]).split()
        
        matched_domains = set()
        for token in tokens:
            if token in self.domain_aliases:
                matched_domains.add(self.domain_aliases[token])

        # Validation: Unknown keyword
        if not matched_domains:
            return {
                "status": "error",
                "error_type": "unknown_keyword",
                "message": "Could not map query to any known Question Registry domains."
            }

        # Validation: Multiple domain matches
        if len(matched_domains) > 1:
            return {
                "status": "error",
                "error_type": "multiple_domain_matches",
                "message": "Search query matched multiple distinct domains. Please be more specific."
            }

        target_domain = matched_domains.pop()

        # Extract all child question IDs matching the domain
        matched_ids = [
            item["question_id"] 
            for item in self.registry_data 
            if item.get("domain_id") == target_domain
        ]

        return {
            "status": "success",
            "matched_domain_id": target_domain,
            "question_ids": matched_ids
        }
