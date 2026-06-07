from fastapi import APIRouter, HTTPException
from concurrent.futures import ThreadPoolExecutor
from repositories.database import busca_sql, busca_sql_um

router = APIRouter(prefix="/cnpj", tags=["CNPJ"])


@router.get("/informacoes/{cnpj}")
def consultar_informacoes(cnpj: str):
    try:
        return busca_sql_um(
            "SELECT * FROM informacoes_cnpj WHERE codigo_favorecido = %s",
            (cnpj,)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/despesas/{cnpj}/resumo")
def consultar_resumo_despesas(cnpj: str):
    try:
        with ThreadPoolExecutor() as ex:
            f_emp = ex.submit(busca_sql_um,
                "SELECT COUNT(*) as total, SUM(valor) as soma FROM empenhos WHERE codigo_favorecido = %s",
                (cnpj,)
            )
            f_liq = ex.submit(busca_sql_um,
                "SELECT COUNT(*) as total, SUM(valor) as soma FROM liquidacoes WHERE codigo_favorecido = %s",
                (cnpj,)
            )
            f_pag = ex.submit(busca_sql_um,
                "SELECT COUNT(*) as total, SUM(valor) as soma FROM pagamentos WHERE codigo_favorecido = %s",
                (cnpj,)
            )

        return {
            "empenhos":    f_emp.result(),
            "liquidacoes": f_liq.result(),
            "pagamentos":  f_pag.result(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/despesas/{cnpj}/empenhos")
def consultar_empenhos(cnpj: str, pagina: int = 0, tamanho: int = 10):
    try:
        return busca_sql(
            """
            SELECT * FROM empenhos
            WHERE codigo_favorecido = %s
            ORDER BY data_emissao DESC
            LIMIT %s OFFSET %s
            """,
            (cnpj, tamanho, pagina * tamanho)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/despesas/{cnpj}/liquidacoes")
def consultar_liquidacoes(cnpj: str, pagina: int = 0, tamanho: int = 10):
    try:
        return busca_sql(
            """
            SELECT * FROM liquidacoes
            WHERE codigo_favorecido = %s
            ORDER BY data_emissao DESC
            LIMIT %s OFFSET %s
            """,
            (cnpj, tamanho, pagina * tamanho)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/despesas/{cnpj}/pagamentos")
def consultar_pagamentos(cnpj: str, pagina: int = 0, tamanho: int = 10):
    try:
        return busca_sql(
            """
            SELECT * FROM pagamentos
            WHERE codigo_favorecido = %s
            ORDER BY data_emissao DESC
            LIMIT %s OFFSET %s
            """,
            (cnpj, tamanho, pagina * tamanho)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notas/{cnpj}")
def consultar_notas(cnpj: str, pagina: int = 0, tamanho: int = 10):
    try:
        total = busca_sql_um(
            "SELECT COUNT(*) as total FROM notas_fiscais WHERE codigo_favorecido = %s",
            (cnpj,)
        )["total"]

        notas = busca_sql(
            """
            SELECT * FROM notas_fiscais
            WHERE codigo_favorecido = %s
            ORDER BY data_emissao DESC
            LIMIT %s OFFSET %s
            """,
            (cnpj, tamanho, pagina * tamanho)
        )

        return {
            "notas":         notas,
            "total":         total,
            "pagina":        pagina,
            "tamanho":       tamanho,
            "total_paginas": -(-total // tamanho)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notas/{cnpj}/itens/{chave}")
def consultar_itens_nota(cnpj: str, chave: str):
    try:
        return busca_sql(
            "SELECT * FROM itens_notas_fiscais WHERE chave_nota = %s",
            (chave,)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))