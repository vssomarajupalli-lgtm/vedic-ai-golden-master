from fastapi import APIRouter
from app.core.logging import log

router = APIRouter()

@router.get("/")
def check_health():
    """
    Basic health check endpoint for load balancers.
    """
    log.info("Health check ping received.")
    return {
        "status": "online",
        "service": "Vedic-AI Core API"
    }
