import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

from repositories.database import verificar_conexao  # noqa: E402
from routes.avaliacao_router import router as avaliacao_router  # noqa: E402
from routes.dados_router import router as dados_router  # noqa: E402
from routes.importacao_router import router as importacao_router  # noqa: E402

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agoradit API",
    version="1.0.0",
    description="API para ingestao e consulta de despesas e notas fiscais.",
)

origens = [
    origem.strip()
    for origem in os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
    if origem.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origens,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Admin-Key"],
)

app.include_router(importacao_router)
app.include_router(dados_router)
app.include_router(avaliacao_router)


@app.get("/health/live", tags=["Health"])
def health_live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["Health"])
def health_ready() -> dict[str, str]:
    verificar_conexao()
    return {"status": "ok"}


@app.exception_handler(Exception)
async def tratar_erro_inesperado(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Erro inesperado em %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor"},
    )
