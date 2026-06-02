from fastapi import FastAPI

from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)
app.include_router(despesas_route)


from integrations import pnpc, portal_transparencia
from repositories import empenho_repo, liquidacao_repo, pagamento_repo
from services import limpar_liquidacao, limpar_pagamento, limpar_empenho


#nota = portal_transparencia.buscar_nota_por_chave("35260567463349000130550010000295471261117423")
#print(gatekeeper.executar_gatekeeper(nota["notaFiscalDTO"]))


for pagamentos, empenhos, liquidacoes in portal_transparencia.buscar_despesas_periodo("20240101","20240131"):
    pagamento_repo.salvar(limpar_pagamento.portal_transparencia(pagamentos))
    empenho_repo.salvar(limpar_empenho.portal_transparencia(empenhos))
    liquidacao_repo.salvar(limpar_liquidacao.portal_transparencia(liquidacoes))