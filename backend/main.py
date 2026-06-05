""""""
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from routes.dados_router import router as dados_router
from routes.importacao_router import router as importacao_router

#SOMENTE PARA TESTE -> depois tem q organizaar 
from routes.auditoria_router import router as auditoria_router

from fastapi.middleware.cors import CORSMiddleware

from repositories import database

app = FastAPI(
    title="Gammes 33 API",
    description="API para ingestão e validação de despesas, contratos e notas fiscais."
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(importacao_router)
app.include_router(dados_router)

"""

#VERSÃO DE TESTES
app.include_router(auditoria_router, prefix="/auditoria", tags=["Testes de Fraude"])

@app.on_event("shutdown")
def shutdown_event():
    database.fechar_threads()



"""


from services.importacoes import portal_transparencia


portal_transparencia.importar_empenhos_csv("20250305","20250405", multithreading=True)


database.fechar_threads()