from repositories.database import cursor, db
from dataclasses import asdict

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