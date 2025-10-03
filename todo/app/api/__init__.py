"""API router aggregation for the application."""

from fastapi import APIRouter

from .endpoints.todos import router as todos_router


api_router = APIRouter()
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])

__all__ = ["api_router"]

