from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# TODO: Import your API routers here when they are created
# from app.api.v1.endpoints import users, projects, chats
# from app.api.v1.api import api_router # We'll create this aggregate router later

# Initialize FastAPI app
app = FastAPI(
    title="Keryx Backend API",
    description="API for organizing LLM-based chats by project with common base instructions.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Keryx Backend API!"}


# TODO: Include the main API router
# app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
