from repositories.database import cursor, db
from dataclasses import asdict


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