from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import traceback

from app.core.config import settings
from app.core.logging import log
from app.api.v1.router import api_router

def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.
    """
    log.info(f"Starting {settings.PROJECT_NAME}...")
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Stateless Astrology Engine API",
        version="1.0.0"
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include the API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Optional direct run block for local development
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
