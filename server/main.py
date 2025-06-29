# server/main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse  # Import RedirectResponse

from app.api.v1.api import api_router  # Import the aggregated API router
from app.core.config import settings  # Import your settings for configuration

# Initialize FastAPI app with settings from config.py
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for organizing LLM-based chats by project with common base instructions.",
    version="1.0.0",
    openapi_url=f"{settings.API_VER_STR}/openapi.json",  # Set OpenAPI URL based on API_VER_STR
)


# Root endpoint to redirect to documentation
@app.get("/")
async def root():  # <--- Changed to async def and uses RedirectResponse
    """
    Redirects to the OpenAPI (Swagger UI) documentation.
    """
    return RedirectResponse(url="/docs")


# Include the main API router with the version prefix
app.include_router(api_router, prefix=settings.API_VER_STR)
