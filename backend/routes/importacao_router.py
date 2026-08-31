from datetime import date
from typing import Annotated, Any

from celery.result import AsyncResult
from core.security import exigir_chave_administrativa
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from worker import (
    celery_app,
    importar_cnpj,
    importar_despesas,
    importar_itens_notas,
    importar_notas,
)

router = APIRouter(
    prefix="/importacao",
    tags=["Importacao"],
    dependencies=[Depends(exigir_chave_administrativa)],
)
DataImportacao = Annotated[date, Query(description="Data no formato YYYY-MM-DD")]


class JobCriado(BaseModel):
    job_id: str
    status: str = "PENDING"


class JobStatus(BaseModel):
    job_id: str
    status: str
    resultado: Any | None = None


def _periodo(data_inicio: date, data_fim: date, limite_dias: int) -> tuple[str, str]:
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="data_fim deve ser igual ou posterior a data_inicio",
        )
    if (data_fim - data_inicio).days > limite_dias:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"O periodo maximo permitido e de {limite_dias} dias",
        )
    return data_inicio.strftime("%Y%m%d"), data_fim.strftime("%Y%m%d")


def _job_criado(resultado: AsyncResult) -> JobCriado:
    return JobCriado(job_id=resultado.id)


@router.post("/cnpj", response_model=JobCriado, status_code=status.HTTP_202_ACCEPTED)
def criar_importacao_cnpj() -> JobCriado:
    return _job_criado(importar_cnpj.delay())


@router.post("/despesas", response_model=JobCriado, status_code=status.HTTP_202_ACCEPTED)
def criar_importacao_despesas(data_inicio: DataImportacao, data_fim: DataImportacao) -> JobCriado:
    inicio, fim = _periodo(data_inicio, data_fim, limite_dias=366)
    return _job_criado(importar_despesas.delay(inicio, fim))


@router.post("/notas", response_model=JobCriado, status_code=status.HTTP_202_ACCEPTED)
def criar_importacao_notas(data_inicio: DataImportacao, data_fim: DataImportacao) -> JobCriado:
    inicio, fim = _periodo(data_inicio, data_fim, limite_dias=3660)
    return _job_criado(importar_notas.delay(inicio, fim))


@router.post("/itens-notas", response_model=JobCriado, status_code=status.HTTP_202_ACCEPTED)
def criar_importacao_itens(data_inicio: DataImportacao, data_fim: DataImportacao) -> JobCriado:
    inicio, fim = _periodo(data_inicio, data_fim, limite_dias=3660)
    return _job_criado(importar_itens_notas.delay(inicio, fim))


@router.get("/jobs/{job_id}", response_model=JobStatus)
def consultar_job(job_id: str) -> JobStatus:
    job = celery_app.AsyncResult(job_id)
    resultado = job.result if job.successful() else None
    return JobStatus(job_id=job.id, status=job.status, resultado=resultado)
