from fastapi import APIRouter
from integrations.portal_transparencia import buscar_notas


router = APIRouter()

@router.get("/notas")
def notas(pagina: int = 1, cnpj: str = None):
    try:
        dados = buscar_notas(pagina, cnpj)
        return dados

    except Exception as e:
        return {
            "erro": str(e)
        }