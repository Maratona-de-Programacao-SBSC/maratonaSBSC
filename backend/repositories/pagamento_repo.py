from repositories.database import cursor, db
from schemes.pagamento import Pagamento
import csv
import tempfile


def salvar(pagamentos):
    dados = [{
        "codigo_pagamento": p.codigo_pagamento,
        "data_emissao": p.data_emissao,
        "codigo_favorecido": p.codigo_favorecido,
        "favorecido": p.favorecido,
        "processo": p.processo,
        "codigo_unidade_gestora": p.codigo_unidade_gestora,
        "unidade_gestora": p.unidade_gestora,
        "codigo_orgao": p.codigo_orgao,
        "orgao": p.orgao,
        "observacao": p.observacao,
        "valor": p.valor,
    } for p in pagamentos]  

    if not dados: return

    query = """INSERT IGNORE INTO pagamentos (codigo_pagamento, data_emissao, codigo_favorecido, favorecido,
                processo, codigo_unidade_gestora, unidade_gestora, codigo_orgao, orgao,
                observacao, valor)
            VALUES (%(codigo_pagamento)s, %(data_emissao)s, %(codigo_favorecido)s, %(favorecido)s,
                %(processo)s, %(codigo_unidade_gestora)s, %(unidade_gestora)s, %(codigo_orgao)s, %(orgao)s,
                %(observacao)s, %(valor)s)"""
    
    cursor.executemany(query, dados)
    db.commit()




def busca_cnpj(cnpj):
    query = """SELECT * FROM pagamentos WHERE codigo_favorecido = %s"""

    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'pagamento'

    return [Pagamento(**d) for d in dados]


def busca_cnpj_dado(cnpj, nome_dado):
    query = f"""SELECT {nome_dado} FROM pagamentos WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;