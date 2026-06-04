from dataclasses import dataclass

@dataclass
class Empenho:
    id_empenho: int
    codigo_empenho: str
    data_emissao: str
    tipo_empenho: str
    codigo_orgao: int
    codigo_unidade_gestora: int
    codigo_favorecido: str
    favorecido: str
    observacao: str
    elemento_despesa: str
    valor: float


PORTAL_TRANSPARENCIA_EMPENHOS_SCHEMA = {
    "tabela": "empenhos",
    "total_colunas": 63,
    "mapa": {
        0:  {"coluna": "id_empenho",              "tipo": "direto"}, # "Id Empenho"
        1:  {"coluna": "codigo_empenho",          "tipo": "direto"}, # "Código Empenho"
        3:  {"coluna": "data_emissao",            "tipo": "data"},   # "Data Emissão"
        6:  {"coluna": "tipo_empenho",            "tipo": "direto"}, # "Tipo Empenho"
        10: {"coluna": "codigo_orgao",            "tipo": "direto"}, # "Código Órgão"
        12: {"coluna": "codigo_unidade_gestora",  "tipo": "direto"}, # "Código Unidade Gestora"
        16: {"coluna": "codigo_favorecido",       "tipo": "direto"}, # "Código Favorecido"
        17: {"coluna": "favorecido",              "tipo": "direto"}, # "Favorecido"
        18: {"coluna": "observacao",              "tipo": "direto"}, # "Observação"
        52: {"coluna": "elemento_despesa",        "tipo": "direto"}, # "Elemento de Despesa" (Índice 52)
        60: {"coluna": "valor",                   "tipo": "valor"}   # "Valor Original do Empenho" (Índice 60)
    }
}
