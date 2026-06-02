from repositories.database import cursor, db
from schemes.empenho import Empenho
import tempfile
import csv



def salvar(empenhos):

    dados = [{
        "id_empenho": e.id_empenho,
        "codigo_empenho": e.codigo_empenho,
        "data_emissao": e.data_emissao,
        "tipo_empenho": e.tipo_empenho,
        "codigo_orgao": e.codigo_orgao,
        "codigo_unidade_gestora": e.codigo_unidade_gestora,
        "codigo_favorecido": e.codigo_favorecido,
        "favorecido": e.favorecido,
        "observacao": e.observacao,
        "elemento_despesa": e.elemento_despesa,
        "valor": e.valor,
    } for e in empenhos]

    if not dados: return

    query = """INSERT IGNORE INTO empenhos (id_empenho, codigo_empenho, data_emissao, tipo_empenho,
                codigo_orgao, codigo_unidade_gestora, codigo_favorecido, favorecido,
                observacao, elemento_despesa, valor)
            VALUES (%(id_empenho)s, %(codigo_empenho)s, %(data_emissao)s, %(tipo_empenho)s,
                %(codigo_orgao)s, %(codigo_unidade_gestora)s, %(codigo_favorecido)s, %(favorecido)s,
                %(observacao)s, %(elemento_despesa)s, %(valor)s)"""
    
    cursor.executemany(query, dados)
    db.commit()

def salvar_varios(empenhos):

    dados = [{
        "id_empenho": e.id_empenho,
        "codigo_empenho": e.codigo_empenho,
        "data_emissao": e.data_emissao,
        "tipo_empenho": e.tipo_empenho,
        "codigo_orgao": e.codigo_orgao,
        "codigo_unidade_gestora": e.codigo_unidade_gestora,
        "codigo_favorecido": e.codigo_favorecido,
        "favorecido": e.favorecido,
        "observacao": e.observacao,
        "elemento_despesa": e.elemento_despesa,
        "valor": e.valor,
    } for e in empenhos]

    if not dados: return

    with tempfile.NamedTemporaryFile(
        mode="w", 
        suffix=".csv", 
        delete=True, 
        encoding="UTF-8", 
        newline="", 
        dir="C:/ProgramData/MySQL/MySQL Server 8.0/Uploads"
        ) as arquivo_csv:

        caminho = arquivo_csv.name.replace("\\", "/")
        escritor = csv.DictWriter(arquivo_csv, fieldnames=dados[0].keys())
        escritor.writeheader()
        escritor.writerows(dados)

        query = f"""LOAD DATA INFILE '{caminho}' IGNORE
                    INTO TABLE empenhos
                    FIELDS TERMINATED BY ','
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\\n'
                    IGNORE 1 ROWS
                    (id_empenho, codigo_empenho, data_emissao, tipo_empenho,
                    codigo_orgao, codigo_unidade_gestora, codigo_favorecido, favorecido,
                    observacao, elemento_despesa, valor)"""

        cursor.execute(query)
        db.commit()

def busca_cnpj(cnpj):
    query = """SELECT * FROM empenhos WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'empenho'

    return [Empenho(**d) for d in dados]


def busca_cnpj_dado_especifico(cnpj, nome_dado):
    query = f"""SELECT {nome_dado} FROM empenhos WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;