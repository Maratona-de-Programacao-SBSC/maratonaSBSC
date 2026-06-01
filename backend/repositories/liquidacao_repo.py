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
        "tipo_documento": l.tipo_documento,
    } for l in liquidacoes]

    query = """INSERT IGNORE INTO liquidacoes (codigo_liquidacao, data_emissao, codigo_orgao,
                codigo_unidade_gestora, codigo_favorecido, favorecido,
                observacao, codigo_elemento_despesa)
            VALUES (%(codigo_liquidacao)s, %(data_emissao)s, %(codigo_orgao)s,
                %(codigo_unidade_gestora)s, %(codigo_favorecido)s, %(favorecido)s,
                %(observacao)s, %(codigo_elemento_despesa)s)"""
    
    cursor.executemany(query, dados)
    db.commit()


def salvar_load_infile(liquidacoes):

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

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=True, encoding="UTF-8", newline="") as arquivo_csv:
        caminho = arquivo_csv.name.replace("\\", "/")
        escritor = csv.DictWriter(arquivo_csv, fieldnames=dados[0].keys())
        escritor.writeheader()
        escritor.writerows(dados)

        query = f"""LOAD DATA LOCAL INFILE '{caminho}'
                    INTO TABLE liquidacoes
                    FIELDS TERMINATED BY ','
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\\n'
                    IGNORE 1 ROWS
                    (codigo_liquidacao, data_emissao, codigo_orgao,
                    codigo_unidade_gestora, codigo_favorecido, favorecido,
                    observacao, codigo_elemento_despesa)"""
                
        cursor.execute(query)
        db.commit()


def busca_cnpj(cnpj):
    query = """SELECT * FROM liquidacoes WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'liquidacao'

    return [Liquidacao(**d) for d in dados]


def busca_cnpj_dado_especifico(cnpj, nome_dado):
    query = f"""SELECT {nome_dado} FROM liquidacoes WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;