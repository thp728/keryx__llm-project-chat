import json
import httpx

from dotenv import load_dotenv
import os

load_dotenv()

API_VER_STR = os.getenv("API_VER_STR")
API_SCHEMA_URL = f"http://localhost:8000{API_VER_STR}/openapi.json"
OUTPUT_FILE = "openapi.json"


async def fetch_and_save_openapi_schema():
    print(f"Attempting to fetch OpenAPI schema from: {API_SCHEMA_URL}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_SCHEMA_URL)
            response.raise_for_status()
            schema_data = response.json()

        with open(OUTPUT_FILE, "w") as f:
            json.dump(schema_data, f, indent=2)
        print(f"OpenAPI schema successfully saved to {OUTPUT_FILE}")

    except httpx.HTTPStatusError as e:
        print(
            f"HTTP error fetching schema: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        print(f"Request error fetching schema: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(fetch_and_save_openapi_schema())
