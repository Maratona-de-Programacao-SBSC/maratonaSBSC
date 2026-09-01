from typing import Annotated, Any

from fastapi import Path, Query
from pydantic import BaseModel

Cnpj = Annotated[
    str,
    Path(
        min_length=14,
        max_length=14,
        pattern=r"^\d{14}$",
        description="CNPJ com 14 digitos, sem pontuacao",
    ),
]
Pagina = Annotated[int, Query(ge=0, description="Pagina iniciada em zero")]
TamanhoPagina = Annotated[int, Query(ge=1, le=100)]


class PaginaNotas(BaseModel):
    notas: list[dict[str, Any]]
    total: int
    pagina: int
    tamanho: int
    total_paginas: int
