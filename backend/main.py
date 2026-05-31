from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from integrations import pnpc, portal_transparencia

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)

@app.get("/")
def home():
    return {"status": "online"}

for pagamento, empenho, liquidacao, pagamento_empenho, empenho_liquidacao in portal_transparencia.busca_despesas_periodo("20250102","20260102"):
    if pagamento:
        print(pagamento[0])