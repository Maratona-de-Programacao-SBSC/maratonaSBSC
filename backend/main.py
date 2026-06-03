import os
from dotenv import load_dotenv

print("\n🔍 === DIAGNÓSTICO DO AMBIENTE ===")
print("1. Pasta onde o Python está rodando:", os.getcwd())
print("2. Arquivos reais que ele está vendo nesta pasta:", os.listdir('.'))

# Tenta carregar e guarda o resultado (True se achou o arquivo, False se não achou)
foi_carregado = load_dotenv()

print(f"3. O python-dotenv encontrou o arquivo '.env'? {foi_carregado}")
print("4. Valor lido para DATABASE_HOST:", os.getenv("DATABASE_HOST"))
print("==================================\n")

from fastapi import FastAPI
# ... resto dos seus imports ...

from fastapi import FastAPI

from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route
from routes.database_router import router as database_router

from integrations import pnpc, portal_transparencia
from repositories import empenho_repo, liquidacao_repo, pagamento_repo
from services import limpar_liquidacao, limpar_pagamento, limpar_empenho

app = FastAPI(
    title="Gammes 33 API",
    description="API para ingestão e validação de despesas, contratos e notas fiscais."
)

app.include_router(notas_route)
app.include_router(contratos_route)
app.include_router(despesas_route)
app.include_router(database_router)

