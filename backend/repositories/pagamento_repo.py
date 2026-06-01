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
        "tipo_documento": p.tipo_documento,
    } for p in pagamentos]  

    query = """INSERT IGNORE INTO pagamentos (codigo_pagamento, data_emissao, codigo_favorecido, favorecido,
                processo, codigo_unidade_gestora, unidade_gestora, codigo_orgao, orgao,
                observacao, valor)
            VALUES (%(codigo_pagamento)s, %(data_emissao)s, %(codigo_favorecido)s, %(favorecido)s,
                %(processo)s, %(codigo_unidade_gestora)s, %(unidade_gestora)s, %(codigo_orgao)s, %(orgao)s,
                %(observacao)s, %(valor)s)"""
    
    cursor.executemany(query, dados)
    db.commit()


def salvar_load_infile(pagamentos):

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
        "tipo_documento": p.tipo_documento,
    } for p in pagamentos]  

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=True, encoding="UTF-8", newline="") as arquivo_csv:
        caminho = arquivo_csv.name.replace("\\", "/")
        escritor = csv.DictWriter(arquivo_csv, fieldnames=dados[0].keys())
        escritor.writeheader()
        escritor.writerows(dados)

        query = f"""LOAD DATA LOCAL INFILE '{caminho}'
                    INTO TABLE pagamentos
                    FIELDS TERMINATED BY ','
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\\n'
                    IGNORE 1 ROWS
                    (codigo_pagamento, data_emissao, codigo_favorecido, favorecido,
                    processo, codigo_unidade_gestora, unidade_gestora, codigo_orgao,
                    orgao, observacao, valor)"""
        
        cursor.execute(query)
        db.commit()



def busca_cnpj(cnpj):
    query = """SELECT * FROM pagamentos WHERE codigo_favorecido = %s"""

    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'pagamento'

    return [Pagamento(**d) for d in dados]


def busca_cnpj_dado_especifico(cnpj, nome_dado):
    query = f"""SELECT {nome_dado} FROM pagamentos WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;