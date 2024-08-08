from fastapi import FastAPI

from src.core.configs import settings
from src.api.v1.api import api_router

app = FastAPI(
    title="API de Cursos (SLDS)",
    description="API para cadastro, consulta, atualização e exclusão de cursos",
    version="0.0.1",
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
