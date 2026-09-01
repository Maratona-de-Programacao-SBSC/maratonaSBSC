from typing import Any

from fastapi import APIRouter, HTTPException, status
from repositories.database import busca_sql, busca_sql_um
from schemes.api import Cnpj, Pagina, PaginaNotas, TamanhoPagina

router = APIRouter(prefix="/cnpj", tags=["CNPJ"])


@router.get("/informacoes/{cnpj}")
def consultar_informacoes(cnpj: Cnpj) -> dict[str, Any]:
    registro = busca_sql_um("SELECT * FROM informacoes_cnpj WHERE codigo_favorecido = %s", (cnpj,))
    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CNPJ nao encontrado",
        )
    return registro


@router.get("/despesas/{cnpj}/resumo")
def consultar_resumo_despesas(cnpj: Cnpj) -> dict[str, dict[str, Any]]:
    registros = busca_sql(
        """
        SELECT 'empenhos' AS tipo, COUNT(*) AS total, COALESCE(SUM(valor), 0) AS soma
        FROM empenhos WHERE codigo_favorecido = %s
        UNION ALL
        SELECT 'liquidacoes', COUNT(*), COALESCE(SUM(valor), 0)
        FROM liquidacoes WHERE codigo_favorecido = %s
        UNION ALL
        SELECT 'pagamentos', COUNT(*), COALESCE(SUM(valor), 0)
        FROM pagamentos WHERE codigo_favorecido = %s
        """,
        (cnpj, cnpj, cnpj),
    )
    return {
        registro["tipo"]: {
            "total": registro["total"],
            "soma": registro["soma"],
        }
        for registro in registros
    }


def _consultar_despesas(tabela: str, cnpj: str, pagina: int, tamanho: int) -> list[dict[str, Any]]:
    tabelas = {"empenhos", "liquidacoes", "pagamentos"}
    if tabela not in tabelas:
        raise ValueError("Tabela de despesas invalida")
    return busca_sql(
        f"""
        SELECT * FROM {tabela}
        WHERE codigo_favorecido = %s
        ORDER BY data_emissao DESC
        LIMIT %s OFFSET %s
        """,
        (cnpj, tamanho, pagina * tamanho),
    )


@router.get("/despesas/{cnpj}/empenhos")
def consultar_empenhos(
    cnpj: Cnpj, pagina: Pagina = 0, tamanho: TamanhoPagina = 10
) -> list[dict[str, Any]]:
    return _consultar_despesas("empenhos", cnpj, pagina, tamanho)


@router.get("/despesas/{cnpj}/liquidacoes")
def consultar_liquidacoes(
    cnpj: Cnpj, pagina: Pagina = 0, tamanho: TamanhoPagina = 10
) -> list[dict[str, Any]]:
    return _consultar_despesas("liquidacoes", cnpj, pagina, tamanho)


@router.get("/despesas/{cnpj}/pagamentos")
def consultar_pagamentos(
    cnpj: Cnpj, pagina: Pagina = 0, tamanho: TamanhoPagina = 10
) -> list[dict[str, Any]]:
    return _consultar_despesas("pagamentos", cnpj, pagina, tamanho)


@router.get("/notas/{cnpj}", response_model=PaginaNotas)
def consultar_notas(cnpj: Cnpj, pagina: Pagina = 0, tamanho: TamanhoPagina = 10) -> PaginaNotas:
    registro_total = busca_sql_um(
        "SELECT COUNT(*) AS total FROM notas_fiscais WHERE codigo_favorecido = %s",
        (cnpj,),
    )
    total = registro_total["total"] if registro_total else 0
    notas = busca_sql(
        """
        SELECT * FROM notas_fiscais
        WHERE codigo_favorecido = %s
        ORDER BY data_emissao DESC
        LIMIT %s OFFSET %s
        """,
        (cnpj, tamanho, pagina * tamanho),
    )
    return PaginaNotas(
        notas=notas,
        total=total,
        pagina=pagina,
        tamanho=tamanho,
        total_paginas=(total + tamanho - 1) // tamanho,
    )


@router.get("/notas/{cnpj}/itens/{chave}")
def consultar_itens_nota(cnpj: Cnpj, chave: str) -> list[dict[str, Any]]:
    return busca_sql(
        """
        SELECT item.*
        FROM itens_notas_fiscais item
        JOIN notas_fiscais nota ON nota.chave_acesso = item.chave_nota
        WHERE item.chave_nota = %s AND nota.codigo_favorecido = %s
        """,
        (chave, cnpj),
    )
