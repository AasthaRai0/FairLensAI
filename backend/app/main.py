"""
Main FastAPI application entry point.
Configures routes, middleware, and startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.config import get_settings
from app.routes import audit, history, report
from app.models import HealthCheck

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI Fairness Audit Platform API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(audit.router, prefix="/api/v1", tags=["audit"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])
app.include_router(report.router, prefix="/api/v1", tags=["report"])


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthCheck(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=datetime.utcnow()
    )


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down application")


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

    explanation, recommendations, verified = gemini_service.generate_explanation_and_recommendations(
    user_id="user_123",
    metrics=metrics,
    protected_attributes=protected_attrs,
    outcome_column=outcome,
    overall_score=score
)

return {
    "score": score,
    "explanation": explanation,
    "recommendations": recommendations,
    "verified": verified   # 🔥 IMPORTANT
}