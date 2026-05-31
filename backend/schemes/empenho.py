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