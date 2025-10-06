"""API router aggregation for the application."""

from fastapi import APIRouter

from .endpoints.todos import router as todos_router
from .endpoints.users import router as users_router


api_router = APIRouter()
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
api_router.include_router(users_router, prefix="/users", tags=["users"])

__all__ = ["api_router"]

