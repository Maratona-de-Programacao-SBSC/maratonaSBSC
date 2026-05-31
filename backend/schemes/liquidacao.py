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
    tipo_documento: str