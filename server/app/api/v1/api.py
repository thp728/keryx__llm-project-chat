from fastapi import APIRouter

from app.api.v1.endpoints import users, projects, chats, login

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(login.router, tags=["login"])
