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


@router.get("/despesas/{cnpj}")
def consultar_despesas(cnpj: str):
    try:
        with ThreadPoolExecutor() as ex:
            f_emp = ex.submit(busca_sql,
                "SELECT * FROM empenhos WHERE codigo_favorecido = %s ORDER BY data_emissao DESC",
                (cnpj,))
            f_liq = ex.submit(busca_sql,
                "SELECT * FROM liquidacoes WHERE codigo_favorecido = %s ORDER BY data_emissao DESC",
                (cnpj,))
            f_pag = ex.submit(busca_sql,
                "SELECT * FROM pagamentos WHERE codigo_favorecido = %s ORDER BY data_emissao DESC",
                (cnpj,))

        return {
            "empenhos":    f_emp.result(),
            "liquidacoes": f_liq.result(),
            "pagamentos":  f_pag.result(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notas/{cnpj}")
def consultar_notas(cnpj: str):
    try:
        notas = busca_sql(
            "SELECT * FROM notas_fiscais WHERE codigo_favorecido = %s ORDER BY data_emissao DESC",
            (cnpj,)
        )

        def buscar_itens(nota):
            itens = busca_sql(
                "SELECT * FROM itens_notas_fiscais WHERE chave_nota = %s",
                (nota["chave_acesso"],)
            )
            return {"nota": nota, "itens": itens}

        with ThreadPoolExecutor(max_workers=10) as ex:
            resultado = list(ex.map(buscar_itens, notas))

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))