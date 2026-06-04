
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NotaFiscal:
    chave_acesso: str
    data_emissao: datetime 
    cpf_cnpj_emitente: str
    razao_social_emitente: str 
    uf_emitente: str
    municipio_emitente: str 
    codigo_orgao_destinatario: int 
    orgao_destinatario: str 
    cnpj_destinatario: str 
    nome_destinatario: str 
    uf_destinatario: str
    destino_operacao: int 
    consumidor_final: int 
    valor: float 


PORTAL_TRANSPARENCIA_NOTA_FISCAL_SCHEMA = {
    "tabela": "notas_fiscais",
    "total_colunas": 25,
    "mapa": {
        0:  {"coluna": "chave_acesso",              "tipo": "direto"}, 
        5:  {"coluna": "data_emissao",              "tipo": "data"},   
        8:  {"coluna": "cpf_cnpj_emitente",         "tipo": "direto"},
        9:  {"coluna": "razao_social_emitente",    "tipo": "direto"},
        11: {"coluna": "uf_emitente",               "tipo": "direto"}, 
        12: {"coluna": "municipio_emitente",        "tipo": "direto"},
        15: {"coluna": "codigo_orgao_destinatario", "tipo": "direto"}, 
        16: {"coluna": "orgao_destinatario",        "tipo": "direto"},
        17: {"coluna": "cnpj_destinatario",         "tipo": "direto"}, 
        18: {"coluna": "nome_destinatario",         "tipo": "direto"},
        19: {"coluna": "uf_destinatario",           "tipo": "direto"}, 
        21: {"coluna": "destino_operacao",          "tipo": "direto"}, 
        22: {"coluna": "consumidor_final",          "tipo": "direto"}, 
        24: {"coluna": "valor",                     "tipo": "valor"} 
    }
}