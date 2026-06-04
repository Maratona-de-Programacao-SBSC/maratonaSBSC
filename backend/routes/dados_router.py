from fastapi import APIRouter
from repositories.database import cursor

router = APIRouter(prefix="/dados", tags=["dados"])


@router.get("/notas-fiscais")
def listar_notas(limit: int = 100):
    cursor.execute("SELECT * FROM notas_fiscais LIMIT %s", (limit,))
    return cursor.fetchall()


@router.get("/notas-fiscais/{chave}")
def nota_por_chave(chave: str):
    cursor.execute(
        "SELECT * FROM notas_fiscais WHERE chave_acesso = %s",
        (chave,)
    )
    return cursor.fetchone()


@router.get("/itens-notas")
def listar_itens(limit: int = 100):
    cursor.execute("SELECT * FROM itens_notas_fiscais LIMIT %s", (limit,))
    return cursor.fetchall()


@router.get("/itens-notas/{chave}")
def itens_por_nota(chave: str):
    cursor.execute(
        "SELECT * FROM itens_notas_fiscais WHERE chave_nota = %s",
        (chave,)
    )
    return cursor.fetchall()


@router.get("/pagamentos")
def listar_pagamentos(limit: int = 100):
    cursor.execute("SELECT * FROM pagamentos LIMIT %s", (limit,))
    return cursor.fetchall()


@router.get("/pagamentos/{codigo}")
def pagamento_por_codigo(codigo: str):
    cursor.execute(
        "SELECT * FROM pagamentos WHERE codigo_pagamento = %s",
        (codigo,)
    )
    return cursor.fetchone()


@router.get("/empenhos")
def listar_empenhos(limit: int = 100):
    cursor.execute("SELECT * FROM empenhos LIMIT %s", (limit,))
    return cursor.fetchall()


@router.get("/empenhos/{codigo}")
def empenho_por_codigo(codigo: str):
    cursor.execute(
        "SELECT * FROM empenhos WHERE codigo_empenho = %s",
        (codigo,)
    )
    return cursor.fetchone()


@router.get("/liquidacoes")
def listar_liquidacoes(limit: int = 100):
    cursor.execute("SELECT * FROM liquidacoes LIMIT %s", (limit,))
    return cursor.fetchall()


@router.get("/liquidacoes/{codigo}")
def liquidacao_por_codigo(codigo: str):
    cursor.execute(
        "SELECT * FROM liquidacoes WHERE codigo_liquidacao = %s",
        (codigo,)
    )
    return cursor.fetchone()


@router.get("/empresas")
def listar_empresas(limit: int = 100):
    cursor.execute("SELECT * FROM empresas LIMIT %s", (limit,))
    return cursor.fetchall()


@router.get("/empresas/{cnpj}")
def empresa_por_cnpj(cnpj: str):
    cursor.execute(
        "SELECT * FROM empresas WHERE codigo_favorecido = %s",
        (cnpj,)
    )
    return cursor.fetchone()


@router.get("/cnpj/{cnpj}")
def buscar_cnpj(cnpj: str):
    resultado = {}

    cursor.execute(
        "SELECT * FROM informacoes_cnpj WHERE codigo_favorecido = %s",
        (cnpj,)
    )
    resultado["empresa"] = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM empenhos WHERE codigo_favorecido = %s LIMIT 100",
        (cnpj,)
    )
    resultado["empenhos"] = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM liquidacoes WHERE codigo_favorecido = %s LIMIT 100",
        (cnpj,)
    )
    resultado["liquidacoes"] = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM pagamentos WHERE codigo_favorecido = %s LIMIT 100",
        (cnpj,)
    )
    resultado["pagamentos"] = cursor.fetchall()

    total_empenhado = sum(e.get("valor", 0) or 0 for e in resultado["empenhos"])
    total_pago = sum(p.get("valor", 0) or 0 for p in resultado["pagamentos"])

    resultado["resumo"] = {
        "total_empenhado": total_empenhado,
        "total_pago": total_pago
    }

    return resultado