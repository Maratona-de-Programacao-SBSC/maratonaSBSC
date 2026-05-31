from schemes.empenho import Empenho
from services import formata

def portal_transparencia(empenhos):
    for empenho in empenhos:
        empenho_filtrado = Empenho(
            id_empenho=int(empenho['Id Empenho']),
            codigo_empenho=empenho['Código Empenho'],
            data_emissao=formata.data(empenho['Data Emissão']),
            tipo_empenho=empenho['Tipo Empenho'],
            codigo_orgao=int(empenho['Código Órgão']) if empenho['Código Órgão'] else None,
            codigo_unidade_gestora=int(empenho['Código Unidade Gestora']) if empenho['Código Unidade Gestora'] else None,
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

def formata_data(data):
    return f"{data[6:10]}-{data[3:5]}-{data[0:2]}"