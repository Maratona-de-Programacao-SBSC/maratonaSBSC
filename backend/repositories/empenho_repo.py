from repositories.database import cursor, db
from dataclasses import asdict
from schemes.empenho import Empenho


def salvar(empenhos):

    dados = [asdict(e) for e in empenhos]


    query = """INSERT IGNORE INTO empenhos (id_empenho, codigo_empenho, data_emissao, tipo_empenho,
                codigo_orgao, codigo_unidade_gestora, codigo_favorecido, favorecido,
                observacao, elemento_despesa, valor)
            VALUES (%(id_empenho)s, %(codigo_empenho)s, %(data_emissao)s, %(tipo_empenho)s,
                %(codigo_orgao)s, %(codigo_unidade_gestora)s, %(codigo_favorecido)s, %(favorecido)s,
                %(observacao)s, %(elemento_despesa)s, %(valor)s)"""
    
    cursor.executemany(query, dados)



    query = """INSERT IGNORE INTO cnpj_codigos (codigo_favorecido, codigo, tipo)
            VALUES (%(codigo_favorecido)s, %(codigo_empenho)s, %(tipo_documento)s)"""
    
    cursor.executemany(query, dados)

    db.commit()

def busca_cnpj(cnpj):
    query = """SELECT empenhos.* FROM cnpj_codigos 
            INNER JOIN empenhos
            ON cnpj_codigos.codigo = empenhos.codigo_empenho
            WHERE cnpj_codigos.codigo_favorecido = %s AND cnpj_codigos.tipo = 'empenho'"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'empenho'

    return [Empenho(**d) for d in dados]

