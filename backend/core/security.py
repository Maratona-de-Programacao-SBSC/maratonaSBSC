import os
import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status


def exigir_chave_administrativa(
    chave: Annotated[str | None, Header(alias="X-Admin-Key")] = None,
) -> None:
    esperada = os.getenv("ADMIN_API_KEY")
    if not esperada:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Importacoes administrativas nao configuradas",
        )
    if chave is None or not secrets.compare_digest(chave, esperada):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencial administrativa invalida",
        )
