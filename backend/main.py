from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)
app.include_router(despesas_route)


from integrations import pnpc, portal_transparencia
from services import limpa_pagamento, limpa_empenho, limpa_liquidacao
from repositories import empenho_repo, liquidacao_repo, pagamento_repo


#nota = portal_transparencia.buscar_nota_por_chave("35260567463349000130550010000295471261117423")
#print(gatekeeper.executar_gatekeeper(nota["notaFiscalDTO"]))


for pagamentos, empenhos, liquidacoes in portal_transparencia.busca_despesas_periodo("20250102","20250202"):

    pagamento_repo.salvar_varios(limpa_pagamento.portal_transparencia(pagamentos))
    empenho_repo.salvar_varios(limpa_empenho.portal_transparencia(empenhos))
    liquidacao_repo.salvar_varios(limpa_liquidacao.portal_transparencia(liquidacoes))