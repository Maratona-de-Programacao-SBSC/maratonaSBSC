from fastapi import FastAPI

from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route
from routes.database_router import router as database_router

from integrations import pnpc, portal_transparencia
from repositories import empenho_repo, liquidacao_repo, pagamento_repo
from services import limpar_liquidacao, limpar_pagamento, limpar_empenho

app = FastAPI()

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

