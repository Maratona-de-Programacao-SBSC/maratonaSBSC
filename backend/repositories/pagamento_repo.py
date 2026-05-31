from repositories.database import cursor, db
from dataclasses import asdict


def salvar(pagamentos):

    dados = [asdict(p) for p in pagamentos]

    query = """INSERT IGNORE INTO pagamentos (codigo_pagamento, data_emissao, codigo_favorecido, favorecido,
                processo, codigo_unidade_gestora, unidade_gestora, codigo_orgao, orgao,
                observacao, valor)
            VALUES (%(codigo_pagamento)s, %(data_emissao)s, %(codigo_favorecido)s, %(favorecido)s,
                %(processo)s, %(codigo_unidade_gestora)s, %(unidade_gestora)s, %(codigo_orgao)s, %(orgao)s,
                %(observacao)s, %(valor)s)"""
    
    cursor.executemany(query, dados)

    db.commit()