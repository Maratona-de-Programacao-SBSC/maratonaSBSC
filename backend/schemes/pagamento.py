from dataclasses import dataclass
from typing import Optional


@dataclass
class Pagamento:
    codigo_pagamento: str
    data_emissao: str
    codigo_favorecido: str
    favorecido: str
    processo: str
    codigo_unidade_gestora: Optional[int]  #pode ser Null
    codigo_orgao: Optional[int] #pode ser Null
    unidade_gestora: str
    orgao: str
    observacao: str
    valor: float