from schemes.liquidacao import Liquidacao
from services import formata

def portal_transparencia(liquidacoes):
    for liquidacao in liquidacoes:
        yield Liquidacao(
            codigo_liquidacao=liquidacao['Código Liquidação'],
            data_emissao=formata.data(liquidacao['Data Emissão']),
            codigo_orgao=int(liquidacao['Código Órgão']) if liquidacao['Código Órgão'] else None,
            codigo_unidade_gestora=int(liquidacao['Código Unidade Gestora']) if liquidacao['Código Unidade Gestora'] else None,
            codigo_favorecido=liquidacao['Código Favorecido'],
            favorecido=liquidacao['Favorecido'],
            observacao=liquidacao['Observação'],
            codigo_elemento_despesa=liquidacao['Código Elemento de Despesa'],
        )
