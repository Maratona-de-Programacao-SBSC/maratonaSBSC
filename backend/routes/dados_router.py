from fastapi import APIRouter
from repositories.database import cursor

router = APIRouter(prefix="/dados", tags=["dados"])


# =========================
# NOTAS FISCAIS
# =========================

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


# =========================
# ITENS NOTAS
# =========================

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


# =========================
# PAGAMENTOS
# =========================

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


# =========================
# EMPENHOS
# =========================

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


# =========================
# LIQUIDAÇÕES
# =========================

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


# =========================
# EMPRESAS
# =========================

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

# =========================
# INFORMAÇÕES CNPJ
# =========================

@router.get("/informacoes-cnpj")
def listar_informacoes_cnpj(limit: int = 100):
    cursor.execute(
        "SELECT * FROM informacoes_cnpj LIMIT %s",
        (limit,)
    )
    return cursor.fetchall()


@router.get("/informacoes-cnpj/{cnpj}")
def informacao_cnpj(cnpj: str):
    cursor.execute(
        """
        SELECT *
        FROM informacoes_cnpj
        WHERE codigo_favorecido = %s
        """,
        (cnpj,)
    )
    return cursor.fetchone()