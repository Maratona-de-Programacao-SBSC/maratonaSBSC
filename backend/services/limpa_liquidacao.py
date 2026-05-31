from schemes.liquidacao import Liquidacao

def portal_transparencia(liquidacoes):
    for liquidacao in liquidacoes:
        liquidacao_filtrada = Liquidacao(
            codigo_liquidacao=liquidacao['Código Liquidação'],
            data_emissao=liquidacao['Data Emissão'],
            codigo_orgao=int(liquidacao['Código Órgão']),
            codigo_unidade_gestora=int(liquidacao['Código Unidade Gestora']),
            codigo_favorecido=liquidacao['Código Favorecido'],
            favorecido=liquidacao['Favorecido'],
            observacao=liquidacao['Observação'],
            codigo_elemento_despesa=liquidacao['Código Elemento de Despesa']
        )
        
        yield liquidacao_filtrada