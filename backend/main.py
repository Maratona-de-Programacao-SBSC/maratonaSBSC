from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)
app.include_router(despesas_route)

#nota = portal_transparencia.buscar_nota_por_chave("35260567463349000130550010000295471261117423")
#print(gatekeeper.executar_gatekeeper(nota["notaFiscalDTO"]))

