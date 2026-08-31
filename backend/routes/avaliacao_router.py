from typing import Annotated, Any

from fastapi import APIRouter, Query
from repositories.database import busca_sql, busca_sql_um, executar_sql
from schemes.api import Cnpj

router = APIRouter(prefix="/avaliacao", tags=["Avaliacao"])


@router.get("/ranking")
def ranking(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> list[dict[str, Any]]:
    return busca_sql(
        """
        SELECT a.cnpj, a.votos_cidadaos, i.razao_social
        FROM avaliacao_cnpjs a
        LEFT JOIN informacoes_cnpj i ON i.codigo_favorecido = a.cnpj
        ORDER BY a.votos_cidadaos DESC
        LIMIT %s
        """,
        (limit,),
    )


@router.get("/{cnpj}")
def consultar_avaliacao(cnpj: Cnpj) -> dict[str, Any]:
    registro = busca_sql_um("SELECT * FROM avaliacao_cnpjs WHERE cnpj = %s", (cnpj,))
    return registro or {"cnpj": cnpj, "votos_cidadaos": 0}


@router.post("/{cnpj}/votar")
def votar(cnpj: Cnpj) -> dict[str, Any]:
    executar_sql(
        """
        INSERT INTO avaliacao_cnpjs (cnpj, votos_cidadaos)
        VALUES (%s, 1)
        ON DUPLICATE KEY UPDATE votos_cidadaos = votos_cidadaos + 1
        """,
        (cnpj,),
    )
    registro = busca_sql_um("SELECT * FROM avaliacao_cnpjs WHERE cnpj = %s", (cnpj,))
    return registro or {"cnpj": cnpj, "votos_cidadaos": 0}
