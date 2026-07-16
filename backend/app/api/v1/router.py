from fastapi import APIRouter
from app.api.v1.endpoints import charts, queries, health, reports, browser, knowledge

api_router = APIRouter()

# Register endpoint sub-routers under the main v1 router
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(charts.router, prefix="", tags=["charts"])
api_router.include_router(reports.router, prefix="", tags=["reports"])
api_router.include_router(queries.router, prefix="", tags=["queries"])
api_router.include_router(browser.router, prefix="/browser", tags=["browser"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])

