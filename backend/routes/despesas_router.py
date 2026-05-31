from fastapi import APIRouter, BackgroundTasks
from integrations import portal_transparencia
from services import limpa_pagamento, limpa_empenho, limpa_liquidacao
from repositories import empenho_repo, liquidacao_repo, pagamento_repo

router = APIRouter(prefix="/despesas", tags=["Despesas"])


def _processar_despesas(data_inicio: str, data_fim: str):
    for pagamentos, empenhos, liquidacoes, _, _ in portal_transparencia.busca_despesas_periodo(data_inicio, data_fim):

        dados = [p for p in limpa_pagamento.portal_transparencia(pagamentos)]
        pagamento_repo.salvar(dados)

        dados = [p for p in limpa_empenho.portal_transparencia(empenhos)]
        empenho_repo.salvar(dados)

        dados = [p for p in limpa_liquidacao.portal_transparencia(liquidacoes)]
        liquidacao_repo.salvar(dados)


@router.post("/importar")
def importar_despesas(data_inicio: str, data_fim: str, background_tasks: BackgroundTasks):
    """
    Dispara a importação de despesas (empenhos, liquidações e pagamentos)
    para o período informado. Roda em background para não travar a requisição.

    Exemplo: POST /despesas/importar?data_inicio=20250102&data_fim=20250202
    """
    background_tasks.add_task(_processar_despesas, data_inicio, data_fim)
    return {
        "status": "importação iniciada",
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "aviso": "O processo roda em background. Pode demorar alguns minutos."
    }