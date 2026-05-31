from dataclasses import dataclass


@dataclass
class Pagamento:
    codigo_pagamento: str
    data_emissao: str
    codigo_favorecido: str
    favorecido: str
    processo: str
    codigo_unidade_gestora: int
    unidade_gestora: str
    codigo_orgao: int
    orgao: str
    observacao: str
    valor: float