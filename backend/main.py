from fastapi import FastAPI
from routes.notas_router import router as notas_route
from routes.contratos_router import router as contratos_route
from routes.despesas_router import router as despesas_route

app = FastAPI()

app.include_router(notas_route)
app.include_router(contratos_route)
app.include_router(despesas_route)

#Falta botar pra ele salvar também o código do outro pelo csv intermediario, ta tarde fica pra amanhã. 

#Entre as notas muito raramente teve pagamento com código do orgão nulo e codigo da unidade gestorna nulo, é meio suspeito? sim

#Ele demorou 3 minutos e 10 segundos pra pegar 1 mês de dados, não é um horror. É sim.