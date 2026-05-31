from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from integrations import pnpc, portal_transparencia
from services import limpa_pagamento, limpa_empenho, limpa_liquidacao
from repositories import empenho_repo, liquidacao_repo, pagamento_repo


app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)

@app.get("/")
def home():
    return {"status": "online"}



for pagamentos, empenhos, liquidacoes, pagamentos_empenhos, empenhos_liquidacoes in portal_transparencia.busca_despesas_periodo("20250102","20250202"):

    dados = [p for p in limpa_pagamento.portal_transparencia(pagamentos)]
    pagamento_repo.salvar(dados)

    
    dados = [p for p in limpa_empenho.portal_transparencia(empenhos)]
    empenho_repo.salvar(dados)

    
    dados = [p for p in limpa_liquidacao.portal_transparencia(liquidacoes)]
    liquidacao_repo.salvar(dados)




    #Falta botar pra ele salvar também o código do outro pelo csv intermediario, ta tarde fica pra amanhã

    #Entre as notas muito raramente teve pagamento com código do orgão nulo e codigo da unidade gestorna nulo, é meio suspeito?

    #Ele demorou 3 minutos e 10 segundos pra pegar 1 mês de dados, não é um horror