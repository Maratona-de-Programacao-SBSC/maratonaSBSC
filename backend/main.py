from fastapi import FastAPI

from routers.notas_router import router as notas_router

app = FastAPI()

app.include_router(notas_router)

@app.get("/")
def home():
    return {"status": "online"}