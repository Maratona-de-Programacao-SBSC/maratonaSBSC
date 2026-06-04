from repositories.database import cursor, db
from schemes.empenho import Empenho
import os


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

def salvar_csv(path):

    query = f"""
    LOAD DATA INFILE '{path}' IGNORE
    INTO TABLE empenhos
    CHARACTER SET latin1
    FIELDS TERMINATED BY ';'
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
    (
        id_empenho,
        codigo_empenho,
        @lixo1,
        @data_emissao,
        @lixo2,
        @lixo3,
        tipo_empenho,
        @lixo4,
        @lixo5,
        @lixo6,
        codigo_orgao,
        @lixo7,
        codigo_unidade_gestora,
        @lixo8,
        @lixo9,
        @lixo10,
        codigo_favorecido,
        favorecido,
        observacao,
        @lixo11,
        @lixo12,
        @lixo13,
        @lixo14,
        @lixo15,
        @lixo16,
        @lixo17,
        @lixo18,
        @lixo19,
        @lixo20,
        @lixo21,
        @lixo22,
        @lixo23,
        @lixo24,
        @lixo25,
        @lixo26,
        @lixo27,
        @lixo28,
        @lixo29,
        @lixo30,
        @lixo31,
        @lixo32,
        @lixo33,
        @lixo34,
        @lixo35,
        @lixo36,
        @lixo37,
        @lixo38,
        @lixo39,
        @lixo40,
        @lixo41,
        elemento_despesa,
        @lixo42,
        @lixo43,
        @lixo44,
        @lixo45,
        @lixo46,
        @lixo47,
        @valor,
        @lixo48
    )
    SET
        data_emissao = STR_TO_DATE(
            @data_emissao,
            '%d/%m/%Y'
        ),

        valor = CAST(
            REPLACE(
                REPLACE(@valor, '.', ''),
                ',', '.'
            ) AS DECIMAL(15,2)
        )
    """


    cursor.execute(query)
    db.commit()

    os.remove(path)


def busca_cnpj(cnpj: str):
    query = """SELECT * FROM empenhos WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = cursor.fetchall()
    for d in dados:
        d['tipo_documento'] = 'empenho'

    return [Empenho(**d) for d in dados]


def busca_cnpj_dado(cnpj: str, nome_dado: str):
    query = f"""SELECT {nome_dado} FROM empenhos WHERE codigo_favorecido = %s"""
    
    cursor.execute(query, (cnpj,))

    dados = [row[nome_dado] for row in cursor.fetchall()]

    return dados;