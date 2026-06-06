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


PORTAL_TRANSPARENCIA_PAGAMENTOS_SCHEMA = {
    "tabela": "pagamentos",
    "total_colunas": 34, # Mantemos o total original para o parser não se perder
    "mapa": {
        0:  {"coluna": "codigo_pagamento",          "tipo": "direto"},
        2:  {"coluna": "data_emissao",              "tipo": "data"},
        9:  {"coluna": "codigo_orgao",              "tipo": "direto"},
        10: {"coluna": "orgao",                     "tipo": "direto"},
        11: {"coluna": "codigo_unidade_gestora",    "tipo": "direto"},
        12: {"coluna": "unidade_gestora",           "tipo": "direto"},
        15: {"coluna": "codigo_favorecido",         "tipo": "cnpj"},
        16: {"coluna": "favorecido",                "tipo": "direto"},
        17: {"coluna": "observacao",                "tipo": "direto"},
        18: {"coluna": "processo",                  "tipo": "direto"},
        31: {"coluna": "valor",                     "tipo": "valor"} 
    }
}