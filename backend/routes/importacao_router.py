# routes/importacao_router.py

from fastapi import APIRouter, Query
from services.importacoes import portal_transparencia
from repositories import database
from datetime import date

router = APIRouter(prefix="/importacao", tags=["importacao"])


@router.post("/cnpj")
def importar_cnpj():
    portal_transparencia.importar_informacoes_cnpj_csv(multithreading=False)
    return {"status": "ok"}


# EMPENHOS + LIQUIDAÇÕES + PAGAMENTOS (mesma base, mesmo período)
@router.post("/despesas")
def importar_despesas(
    data_inicio: str = Query(...),
    data_fim: str = Query(...)
):
    portal_transparencia.importar_empenhos_csv(
        data_inicio, data_fim, multithreading=True
    )

    portal_transparencia.importar_liquidacoes_csv(
        data_inicio, data_fim, multithreading=True
    )

    portal_transparencia.importar_pagamentos_csv(
        data_inicio, data_fim, multithreading=True
    )

    return {"status": "ok"}


# NOTAS + ITENS (fluxo separado)
@router.post("/notas")
def importar_notas(data_inicio: date, data_fim: date):
    portal_transparencia.importar_notas_fiscais_csv(
        data_inicio.strftime("%Y%m%d"),
        data_fim.strftime("%Y%m%d"),
        multithreading=False
    )
    return {"status": "ok"}


@router.post("/itens-notas")
def importar_itens(data_inicio: date, data_fim: date):
    portal_transparencia.importar_itens_notas_fiscais_csv(
        data_inicio.strftime("%Y%m%d"),
        data_fim.strftime("%Y%m%d"),
        multithreading=True
    )
    return {"status": "ok"}


@router.post("/finalizar")
def finalizar():
    database.fechar_threads()
    return {"status": "fechado"}