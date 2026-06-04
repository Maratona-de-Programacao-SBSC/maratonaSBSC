""""""
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

#from routes.notas_router import router as notas_route
#from routes.contratos_router import router as contratos_route
#from routes.despesas_router import router as despesas_route
#from routes.database_router import router as database_router

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

#app.include_router(notas_route)
#app.include_router(contratos_route)
#app.include_router(despesas_route)
#app.include_router(database_router)





from services import importacoes
from services.decorators import tempo_execucao

#importacoes.importar_notas_fiscais_csv("20240501","20260101", multithreading=True)


importacoes.importar_itens_notas_fiscais_csv("20240501","20250601", multithreading=True)



database.fechar_esteira()


