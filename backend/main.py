
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route
from routes.database_router import router as database_router

from repositories import database

app = FastAPI(
    title="Gammes 33 API",
    description="API para ingestão e validação de despesas, contratos e notas fiscais."
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notas_route)
app.include_router(contratos_route)
app.include_router(despesas_route)
app.include_router(database_router)



import time


import time

"""
inicio = time.time()


for pagamentos, empenhos, liquidacoes in portal_transparencia.buscar_despesas_periodo("20250102", "20250202"):
    pagamento_repo.salvar(limpar_pagamento.portal_transparencia(pagamentos))


    empenho_repo.salvar(limpar_empenho.portal_transparencia(empenhos))

    liquidacao_repo.salvar(limpar_liquidacao.portal_transparencia(liquidacoes))


fim = time.time()

print(f"Tempo: {fim - inicio:.2f} segundos")
"""

inicio = time.time()

from services import importacoes
from repositories import pagamento_repo

#importacoes.importar_liquidacoes("20250201","20250301",multithreading=True)



fim = time.time()

print(pagamento_repo.busca_cnpj("00681882000106"))


database.fechar_esteira()

print(f"Tempo: {fim - inicio:.2f} segundos")

