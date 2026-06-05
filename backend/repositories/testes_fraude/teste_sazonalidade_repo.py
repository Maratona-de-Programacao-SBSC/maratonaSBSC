from repositories.database import cursor, db

def busca_sazonalidade_suspeita() -> list:
    """
    Busca CNPJs onde 90% ou mais das suas liquidações ocorreram no mês de Dezembro.
    """
    query = """
        SELECT 
            l.codigo_favorecido AS cnpj,
            COUNT(l.codigo_liquidacao) AS total_liquidacoes,
            SUM(CASE WHEN MONTH(l.data_emissao) = 12 THEN 1 ELSE 0 END) AS liquidacoes_dezembro
        FROM liquidacoes l
        LEFT JOIN avaliacao_cnpjs a ON l.codigo_favorecido = a.cnpj
        WHERE l.codigo_favorecido IS NOT NULL
          AND l.codigo_favorecido REGEXP '^[0-9]+$'
          AND (a.teste_sazonalidade_dezembro IS NULL OR a.teste_sazonalidade_dezembro = 0)
        GROUP BY l.codigo_favorecido
        HAVING COUNT(l.codigo_liquidacao) >= 3 
           AND (SUM(CASE WHEN MONTH(l.data_emissao) = 12 THEN 1 ELSE 0 END) / COUNT(l.codigo_liquidacao)) >= 0.90
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    query = """
        INSERT INTO avaliacao_cnpjs (
            cnpj, teste_sazonalidade_dezembro, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_sazonalidade_dezembro = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()