from repositories.database import cursor, db
from schemes.liquidacao import Liquidacao
import tempfile
import csv

def salvar(liquidacoes):

    dados = [{
        "codigo_liquidacao": l.codigo_liquidacao,
        "data_emissao": l.data_emissao,
        "codigo_orgao": l.codigo_orgao,
        "codigo_unidade_gestora": l.codigo_unidade_gestora,
        "codigo_favorecido": l.codigo_favorecido,
        "favorecido": l.favorecido,
        "observacao": l.observacao,
        "codigo_elemento_despesa": l.codigo_elemento_despesa,
    } for l in liquidacoes]

    if not dados: return

    query = """INSERT IGNORE INTO liquidacoes (codigo_liquidacao, data_emissao, codigo_orgao,
                codigo_unidade_gestora, codigo_favorecido, favorecido,
                observacao, codigo_elemento_despesa)
            VALUES (%(codigo_liquidacao)s, %(data_emissao)s, %(codigo_orgao)s,
                %(codigo_unidade_gestora)s, %(codigo_favorecido)s, %(favorecido)s,
                %(observacao)s, %(codigo_elemento_despesa)s)"""
    
    cursor.executemany(query, dados)
    db.commit()


def busca_cnpj(cnpj):
    query = """SELECT * FROM liquidacoes WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'liquidacao'

    return [Liquidacao(**d) for d in dados]


def busca_cnpj_dado(cnpj, nome_dado):
    query = f"""SELECT {nome_dado} FROM liquidacoes WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;