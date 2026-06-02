from fastapi import APIRouter
from repositories.database import cursor

router = APIRouter(prefix="/db", tags=["Database"])


@router.get("/notas")
def listar_notas(status: str = None, limite: int = 100, pagina: int = 1):
    offset = (pagina - 1) * limite

    if status:
        cursor.execute(
            "SELECT * FROM notas_fiscais WHERE status = %s LIMIT %s OFFSET %s",
            (status, limite, offset)
        )
    else:
        cursor.execute(
            "SELECT * FROM notas_fiscais LIMIT %s OFFSET %s",
            (limite, offset)
        )

    return cursor.fetchall()


@router.get("/notas/{chave_acesso}/itens")
def listar_itens_nota(chave_acesso: str):
    cursor.execute(
        "SELECT * FROM itens_notas_fiscais WHERE chave_nota = %s",
        (chave_acesso,)
    )
    return cursor.fetchall()


@router.get("/empenhos")
def listar_empenhos(limite: int = 100, pagina: int = 1):
    offset = (pagina - 1) * limite
    cursor.execute("SELECT * FROM empenhos LIMIT %s OFFSET %s", (limite, offset))
    return cursor.fetchall()


@router.get("/pagamentos")
def listar_pagamentos(limite: int = 100, pagina: int = 1):
    offset = (pagina - 1) * limite
    cursor.execute("SELECT * FROM pagamentos LIMIT %s OFFSET %s", (limite, offset))
    return cursor.fetchall()


@router.get("/liquidacoes")
def listar_liquidacoes(limite: int = 100, pagina: int = 1):
    offset = (pagina - 1) * limite
    cursor.execute("SELECT * FROM liquidacoes LIMIT %s OFFSET %s", (limite, offset))
    return cursor.fetchall()