from fastapi import APIRouter, BackgroundTasks
from services import limpar_liquidacao, limpar_pagamento, limpar_empenho
from integrations import portal_transparencia
from repositories import empenho_repo, liquidacao_repo, pagamento_repo

router = APIRouter(prefix="/despesas", tags=["Despesas"])

def _processar_despesas(data_inicio: str, data_fim: str):

    for pagamentos, empenhos, liquidacoes, _, _ in portal_transparencia.buscar_despesas_periodo(data_inicio, data_fim):


        dados = [p for p in limpar_pagamento.portal_transparencia(pagamentos)]
        pagamento_repo.salvar(dados)

        dados = [p for p in limpar_empenho.portal_transparencia(empenhos)]
        empenho_repo.salvar(dados)

        dados = [p for p in limpar_liquidacao.portal_transparencia(liquidacoes)]
        liquidacao_repo.salvar(dados)

@router.post("/importar")
def importar_despesas(data_inicio: str, data_fim: str, background_tasks: BackgroundTasks):
    """
    Dispara a importação de despesas (empenhos, liquidações e pagamentos)
    para o período informado. Roda em background para não travar a requisição.
    """
    background_tasks.add_task(_processar_despesas, data_inicio, data_fim)
    return {
        "status": "importação iniciada",
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "aviso": "O processo roda em background. Pode demorar alguns minutos."
    }