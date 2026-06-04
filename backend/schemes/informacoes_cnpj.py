
from dataclasses import dataclass

@dataclass
class Empresa:
    codigo_favorecido: str
    razao_social: str
    nome_fantasia: str
    cod_cnae: str
    cod_natjuridica: str
    tipo_pessoa: str
    logradouro: str
    numero: str
    complemento: str
    cep: str
    bairro: str
    municipio: str
    uf: str


PORTA_TRANSPARENCIA_INFORMACOES_CNPJ_SCHEMA = {
    "tabela": "informacoes_cnpj",
    "total_colunas": 13,
    "mapa": {
        0:  {"coluna": "codigo_favorecido",     "tipo": "direto"},
        1:  {"coluna": "razao_social",          "tipo": "direto"},
        2:  {"coluna": "nome_fantasia",         "tipo": "direto"},
        3:  {"coluna": "cod_cnae",              "tipo": "direto"},
        4:  {"coluna": "cod_natjuridica",       "tipo": "direto"},
        5:  {"coluna": "tipo_pessoa",           "tipo": "direto"},
        6:  {"coluna": "logradouro",            "tipo": "direto"},
        7:  {"coluna": "numero",                "tipo": "direto"},
        8:  {"coluna": "complemento",           "tipo": "direto"},
        9:  {"coluna": "cep",                   "tipo": "direto"},
        10: {"coluna": "bairro",                "tipo": "direto"},
        11: {"coluna": "municipio",             "tipo": "direto"},
        12: {"coluna": "uf",                    "tipo": "direto"}
    }
}