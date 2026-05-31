from schemes.pagamento import Pagamento



def portal_transparencia(pagamentos):

    #fazer um generator usando list generator

    for pagamento in pagamentos:
        
        pagamento_filtrado = Pagamento(
            codigo_pagamento=pagamento['Código Pagamento'],
            data_emissao=pagamento['Data Emissão'],
            codigo_favorecido=pagamento['Código Favorecido'],
            favorecido=pagamento['Favorecido'],
            processo=pagamento['Processo'],
            codigo_unidade_gestora=int(pagamento['Código Unidade Gestora']),
            unidade_gestora=pagamento['Unidade Gestora'],
            codigo_orgao=int(pagamento['Código Órgão']),
            orgao=pagamento['Órgão'],
            observacao=pagamento['Observação'],
            valor=float(
                pagamento['Valor do Pagamento Convertido pra R$']
                .replace('.', '')
                .replace(',', '.')
            )
        )

        yield pagamento_filtrado



