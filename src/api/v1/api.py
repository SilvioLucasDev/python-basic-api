from fastapi import APIRouter

from src.api.v1.endpoints import courses

api_router = APIRouter()
api_router.include_router(courses.router, prefix="/courses", tags=["Cursos"])
