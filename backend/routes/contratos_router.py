from fastapi import APIRouter, HTTPException, Query
from integrations.pnpc import buscar_contratos

router = APIRouter(prefix="/contratos", tags=["Contratos"])

@router.get("/")
def listar_contratos(
    data_inicial: str = Query(..., example="20250301"),
    data_final: str = Query(..., example="20260301"),
    modalidade: int = Query(default=5),
    pagina: int = Query(default=1, ge=1),
    tamanho: int = Query(default=10, ge=1, le=50),
):
    try:
        return buscar_contratos(data_inicial, data_final, modalidade, pagina, tamanho)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))