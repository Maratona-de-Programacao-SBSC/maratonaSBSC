import os

from celery import Celery
from services.importacoes import portal_transparencia

celery_app = Celery(
    "agoradit",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    result_expires=86400,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(name="importacao.cnpj")
def importar_cnpj() -> dict[str, str]:
    portal_transparencia.importar_informacoes_cnpj_csv(multithreading=False)
    return {"tipo": "cnpj", "status": "concluido"}


@celery_app.task(name="importacao.despesas")
def importar_despesas(data_inicio: str, data_fim: str) -> dict[str, str]:
    portal_transparencia.importar_empenhos_csv(data_inicio, data_fim, multithreading=True)
    portal_transparencia.importar_liquidacoes_csv(data_inicio, data_fim, multithreading=True)
    portal_transparencia.importar_pagamentos_csv(data_inicio, data_fim, multithreading=True)
    return {"tipo": "despesas", "status": "concluido"}


@celery_app.task(name="importacao.notas")
def importar_notas(data_inicio: str, data_fim: str) -> dict[str, str]:
    portal_transparencia.importar_notas_fiscais_csv(data_inicio, data_fim, multithreading=True)
    return {"tipo": "notas", "status": "concluido"}


@celery_app.task(name="importacao.itens_notas")
def importar_itens_notas(data_inicio: str, data_fim: str) -> dict[str, str]:
    portal_transparencia.importar_itens_notas_fiscais_csv(
        data_inicio, data_fim, multithreading=True
    )
    return {"tipo": "itens_notas", "status": "concluido"}
