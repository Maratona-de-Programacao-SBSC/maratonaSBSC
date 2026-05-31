from repositories.database import cursor, db
from dataclasses import asdict
from schemes.pagamento import Pagamento


def salvar(pagamentos):

    dados = [asdict(p) for p in pagamentos]

    query = """INSERT IGNORE INTO pagamentos (codigo_pagamento, data_emissao, codigo_favorecido, favorecido,
                processo, codigo_unidade_gestora, unidade_gestora, codigo_orgao, orgao,
                observacao, valor)
            VALUES (%(codigo_pagamento)s, %(data_emissao)s, %(codigo_favorecido)s, %(favorecido)s,
                %(processo)s, %(codigo_unidade_gestora)s, %(unidade_gestora)s, %(codigo_orgao)s, %(orgao)s,
                %(observacao)s, %(valor)s)"""
    
    cursor.executemany(query, dados)


    query = """INSERT IGNORE INTO cnpj_codigos (codigo_favorecido, codigo, tipo)
            VALUES (%(codigo_favorecido)s, %(codigo_pagamento)s, %(tipo_documento)s)"""
    
    cursor.executemany(query, dados)
    

    db.commit()


def busca_cnpj(cnpj):
    query = """SELECT pagamentos.* FROM cnpj_codigos 
            INNER JOIN pagamentos
            ON cnpj_codigos.codigo = pagamentos.codigo_pagamento
            WHERE cnpj_codigos.codigo_favorecido = %s AND cnpj_codigos.tipo = 'pagamento'"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'pagamento'

    return [Pagamento(**d) for d in dados]