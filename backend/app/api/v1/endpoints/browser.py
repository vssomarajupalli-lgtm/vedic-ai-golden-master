from fastapi import APIRouter, HTTPException
from typing import Any, List, Dict
import traceback
from pydantic import BaseModel, Field

from app.core.registry_loader import QuestionRegistryLoader
from app.core.preferences_manager import PreferencesManager, PreferencesManagerError
from app.core.search_layer import SearchLayer
from app.core.logging import log

router = APIRouter()

# Instantiate the stateless modules
loader = QuestionRegistryLoader()
preferences_manager = PreferencesManager(loader=loader)
search_layer = SearchLayer(loader=loader)

class SearchRequest(BaseModel):
    query: str = Field(..., description="Free text search query")

@router.get("/registry", response_model=List[Dict[str, Any]])
def get_registry() -> Any:
    """Returns the full Question Registry array for the frontend to build the domain accordion."""
    try:
        # Pre-load to ensure fresh state if needed, though loader caches it
        registry_data = loader.load_registry()
        return registry_data
    except Exception as e:
        log.error(f"Error fetching registry: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
def search_questions(request: SearchRequest) -> Any:
    """Resolves free text into Question IDs using the Search Layer."""
    try:
        result = search_layer.resolve(request.query)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error searching questions: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/favorites", response_model=List[Dict[str, Any]])
def get_favorites() -> Any:
    """Returns the user's favorite questions."""
    return preferences_manager.list_favorites()

class FavoriteRequest(BaseModel):
    question_id: str

@router.post("/favorites")
def add_favorite(request: FavoriteRequest) -> Any:
    """Adds a question to favorites."""
    try:
        return preferences_manager.add_favorite(request.question_id)
    except PreferencesManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log.error(f"Error adding favorite: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/favorites/{question_id}")
def remove_favorite(question_id: str) -> Any:
    """Removes a question from favorites."""
    try:
        success = preferences_manager.remove_favorite(question_id)
        return {"status": "success", "removed": success}
    except PreferencesManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log.error(f"Error removing favorite: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recents", response_model=List[Dict[str, Any]])
def get_recents() -> Any:
    """Returns the user's recently asked questions."""
    return preferences_manager.list_recents()
