from dataclasses import dataclass


@dataclass
class Liquidacao:
    codigo_liquidacao: str
    data_emissao: str
    codigo_orgao: int
    codigo_unidade_gestora: int
    codigo_favorecido: str
    favorecido: str
    observacao: str
    codigo_elemento_despesa: str


PORTAL_TRANSPARENCIA_LIQUIDACOES_SCHEMA = {
    "tabela": "liquidacoes",
    "total_colunas": 28,
    "mapa": {
        0: {"coluna": "codigo_liquidacao", "tipo": "direto"},  # "Código Liquidação"
        2: {"coluna": "data_emissao", "tipo": "data"},  # "Data Emissão"
        7: {"coluna": "codigo_orgao", "tipo": "direto"},  # "Código Órgão"
        9: {"coluna": "codigo_unidade_gestora", "tipo": "direto"},  # "Código Unidade Gestora"
        13: {"coluna": "codigo_favorecido", "tipo": "cnpj"},  # "Código Favorecido"
        14: {"coluna": "favorecido", "tipo": "direto"},  # "Favorecido"
        15: {"coluna": "observacao", "tipo": "direto"},  # "Observação"
        22: {"coluna": "codigo_elemento_despesa", "tipo": "direto"},  # "Código Elemento de Despesa"
    },
}

PORTAL_TRANSPARENCIA_LIQUIDACAO_EMPENHOS_SCHEMA = {
    "tabela": "liquidacoes",
    "total_colunas": 8,
    "mapa": {
        0: {"coluna": "codigo_liquidacao", "tipo": "substitui"},  # "Código Liquidação"
        4: {"coluna": "valor_liquidado", "tipo": "valor"},  # "Valor Liquidado (R$)"
    },
}
