from fastapi import APIRouter, Depends
from app.core.logging import log
from app.pipeline_runner import PipelineRunner

router = APIRouter()


@router.get("/")
def check_health():
    """
    Basic health check endpoint for load balancers.
    Returns 200 OK if service is running.
    """
    log.info("Health check ping received.")
    return {
        "status": "online",
        "service": "Vedic-AI Core API"
    }


@router.get("/ready")
def check_readiness():
    """
    Readiness check - verifies all engines are initialized and calibrated.
    """
    try:
        runner = PipelineRunner()
        
        # Verify critical engines are accessible
        engines_status = {
            "planet_strength": runner.planet_engine is not None,
            "house_strength": runner.house_engine is not None,
            "varga": runner.varga_engine is not None,
            "dasha": runner.dasha_engine is not None,
            "rasi_strength": runner.rasi_engine is not None,
            "ashtakavarga": runner.av_engine is not None,
            "transit": runner.transit_engine is not None,
            "natal_promise": runner.natal_engine is not None,
            "master_probability": runner.master_engine is not None,
        }
        
        all_ready = all(engines_status.values())
        
        log.info("Readiness check completed", extra={"engines": engines_status})
        
        return {
            "status": "ready" if all_ready else "degraded",
            "engines": engines_status,
            "calibration_profile": "v1.0_current"
        }
    except Exception as e:
        log.error("Readiness check failed", extra={"error": str(e)})
        return {
            "status": "not_ready",
            "error": str(e)
        }


@router.get("/live")
def check_liveness():
    """
    Liveness check - minimal check for container orchestration.
    """
    return {"status": "alive"}
