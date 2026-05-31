from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from integrations import pnpc, portal_transparencia
from services import limpa_pagamento, limpa_empenho, limpa_liquidacao
from repositories import pagamento

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)

@app.get("/")
def home():
    return {"status": "online"}



for pagamentos, empenhos, liquidacoes, pagamentos_empenhos, empenhos_liquidacoes in portal_transparencia.busca_despesas_periodo("20250102","20250106"):

    dados = [p for p in limpa_pagamento.portal_transparencia(pagamentos)]
    pagamento.salvar(dados)