from repositories.database import cursor, db
from schemes.liquidacao import Liquidacao
import os

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
    
def salvar_csv(path):

    query = f"""
        LOAD DATA INFILE '{path}' IGNORE
        INTO TABLE liquidacoes
        CHARACTER SET latin1
        FIELDS TERMINATED BY ';'
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        (
            codigo_liquidacao,
            @lixo1,
            @data_emissao,
            @lixo2,
            @lixo3,
            @lixo4,
            @lixo5,
            codigo_orgao,
            @lixo6,
            codigo_unidade_gestora,
            @lixo7,
            @lixo8,
            @lixo9,
            codigo_favorecido,
            favorecido,
            observacao,
            @lixo10,
            @lixo11,
            @lixo12,
            @lixo13,
            @lixo14,
            @lixo15,
            codigo_elemento_despesa,
            @lixo16,
            @lixo17,
            @lixo18,
            @lixo19,
            @lixo20
        )
        SET
            data_emissao = STR_TO_DATE(@data_emissao, '%d/%m/%Y')
        """

    cursor.execute(query)
    db.commit()

    os.remove(path)

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