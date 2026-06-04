from dataclasses import dataclass


@dataclass
class ItemNotaFiscal:
    chave_nota: str
    numero_produto: int
    descricao: str
    codigo_ncm: str
    ncm_tipo: str
    cfop: str
    quantidade: float
    unidade: str
    valor_unitario: float
    valor_total: float


PORTAL_TRANSPARENCIA_ITEM_NOTA_FISCAL_SCHEMA = {
    "tabela": "itens_notas_fiscais",
    "total_colunas": 31,
    "mapa": {
        0:  {"coluna": "chave_nota",      "tipo": "direto"},
        22: {"coluna": "numero_produto",  "tipo": "direto"},
        23: {"coluna": "descricao",       "tipo": "direto"},
        24: {"coluna": "codigo_ncm",      "tipo": "direto"},
        25: {"coluna": "ncm",             "tipo": "direto"}, # Nome corrigido para bater com o SQL
        26: {"coluna": "cfop",            "tipo": "direto"},
        27: {"coluna": "quantidade",      "tipo": "valor"},
        28: {"coluna": "unidade",         "tipo": "direto"},
        29: {"coluna": "valor_unitario",  "tipo": "valor"},
        30: {"coluna": "valor",           "tipo": "valor"}   # Nome corrigido para bater com o SQL
    }
}