from repositories.database import cursor, db
from dataclasses import asdict
from schemes.liquidacao import Liquidacao

def salvar(liquidacoes):

    dados = [asdict(l) for l in liquidacoes]

    query = """INSERT IGNORE INTO liquidacoes (codigo_liquidacao, data_emissao, codigo_orgao,
                codigo_unidade_gestora, codigo_favorecido, favorecido,
                observacao, codigo_elemento_despesa)
            VALUES (%(codigo_liquidacao)s, %(data_emissao)s, %(codigo_orgao)s,
                %(codigo_unidade_gestora)s, %(codigo_favorecido)s, %(favorecido)s,
                %(observacao)s, %(codigo_elemento_despesa)s)"""
    
    cursor.executemany(query, dados)


    query = """INSERT IGNORE INTO cnpj_codigos (codigo_favorecido, codigo, tipo)
            VALUES (%(codigo_favorecido)s, %(codigo_liquidacao)s, %(tipo_documento)s)"""
    
    cursor.executemany(query, dados)

    db.commit()

def busca_cnpj(cnpj):
    query = """SELECT liquidacoes.* FROM cnpj_codigos 
            INNER JOIN liquidacoes
            ON cnpj_codigos.codigo = liquidacoes.codigo_liquidacao
            WHERE cnpj_codigos.codigo_favorecido = %s AND cnpj_codigos.tipo = 'liquidacao'"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'liquidacao'

    return [Liquidacao(**d) for d in dados]