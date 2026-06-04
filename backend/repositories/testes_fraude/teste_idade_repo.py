from repositories.database import cursor, db

def busca_cnpjs_para_teste() -> list:
    """
    Busca os CNPJs únicos e a data da sua PRIMEIRA nota fiscal.
    Filtra no próprio SQL para NÃO trazer CNPJs que já falharam neste teste.
    """
    query = """
        SELECT 
            nf.codigo_favorecido AS cnpj, 
            MIN(nf.data_emissao) AS primeira_emissao
        FROM notas_fiscais nf
        LEFT JOIN auditoria_cnpjs a ON nf.codigo_favorecido = a.cnpj
        WHERE (a.teste_idade_empresa IS NULL OR a.teste_idade_empresa = 0)
          AND nf.codigo_favorecido IS NOT NULL
        GROUP BY nf.codigo_favorecido
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Salva O CNPJ na tabela de auditoria apenas se ele falhou.
    Se ele já existir lá (por ter falhado em outro teste), apenas atualiza o score.
    """
    query = """
        INSERT INTO auditoria_cnpjs (
            cnpj, teste_idade_empresa, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_idade_empresa = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()