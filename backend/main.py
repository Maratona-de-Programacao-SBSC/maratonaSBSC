from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)

@app.get("/")
def home():
    return {"status": "online"}