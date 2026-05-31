
from schemes.empenho import Empenho

def portal_transparencia(empenhos):
    for empenho in empenhos:
        empenho_filtrado = Empenho(
            id_empenho=int(empenho['Id Empenho']),
            codigo_empenho=empenho['Código Empenho'],
            data_emissao=empenho['Data Emissão'],
            tipo_empenho=empenho['Tipo Empenho'],
            codigo_orgao=int(empenho['Código Órgão']),
            codigo_unidade_gestora=int(empenho['Código Unidade Gestora']),
            codigo_favorecido=empenho['Código Favorecido'],
            favorecido=empenho['Favorecido'],
            observacao=empenho['Observação'],
            elemento_despesa=empenho['Elemento de Despesa'],
            valor=float(
                empenho['Valor do Empenho Convertido pra R$']
                .replace('.', '')
                .replace(',', '.')
            )
        )
        yield empenho_filtrado