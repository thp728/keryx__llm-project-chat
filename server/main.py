from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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


# TODO: Include API routers here (e.g., app.include_router(api_router, prefix="/api/v1"))
# This will be done once the api/v1/endpoints are set up.

if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
