from schemes.pagamento import Pagamento
from services import formata

def portal_transparencia(pagamentos):
    for pagamento in pagamentos:
        pagamento_filtrado = Pagamento(
            codigo_pagamento=pagamento['Código Pagamento'],
            data_emissao=formata.data(pagamento['Data Emissão']),
            codigo_favorecido=pagamento['Código Favorecido'],
            favorecido=pagamento['Favorecido'],
            processo=pagamento['Processo'],
            codigo_unidade_gestora=int(pagamento['Código Unidade Gestora']) if pagamento['Código Unidade Gestora'] else None,
            unidade_gestora=pagamento['Unidade Gestora'],
            codigo_orgao=int(pagamento['Código Órgão']) if pagamento['Código Órgão'] else None,
            orgao=pagamento['Órgão'],
            observacao=pagamento['Observação'],
            valor=float(
                pagamento['Valor do Pagamento Convertido pra R$']
                .replace('.', '')
                .replace(',', '.')
            ),
            tipo_documento="pagamento"
        )


        yield pagamento_filtrado


