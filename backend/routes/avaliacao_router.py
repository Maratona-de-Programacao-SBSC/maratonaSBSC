from fastapi import APIRouter, HTTPException
from repositories.database import busca_sql_um, busca_sql

router = APIRouter(prefix="/avaliacao", tags=["Avaliação"])

@router.get("/ranking")
def ranking(limit: int = 10):
    try:
        rows = busca_sql(
            """
            SELECT a.cnpj, a.votos_cidadaos, i.razao_social
            FROM avaliacao_cnpjs a
            LEFT JOIN informacoes_cnpj i ON i.codigo_favorecido = a.cnpj
            ORDER BY a.votos_cidadaos DESC
            LIMIT %s
            """,
            (limit,)
        )
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{cnpj}")
def consultar_avaliacao(cnpj: str):
    try:
        row = busca_sql_um(
            "SELECT * FROM avaliacao_cnpjs WHERE cnpj = %s",
            (cnpj,)
        )
        if not row:
            return {"cnpj": cnpj, "votos_cidadaos": 0}
        return row
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{cnpj}/votar")
def votar(cnpj: str):
    try:
        busca_sql(
            """
            INSERT INTO avaliacao_cnpjs (cnpj, votos_cidadaos)
            VALUES (%s, 1)
            ON DUPLICATE KEY UPDATE votos_cidadaos = votos_cidadaos + 1
            """,
            (cnpj,)
        )
        row = busca_sql_um(
            "SELECT * FROM avaliacao_cnpjs WHERE cnpj = %s",
            (cnpj,)
        )
        return row
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))