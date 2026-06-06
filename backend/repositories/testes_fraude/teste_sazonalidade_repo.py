from repositories.database import cursor, db

def busca_sazonalidade_suspeita() -> list:
    """
    Busca CNPJs onde 90% ou mais das suas liquidações ocorreram no mês de Dezembro.
    """
    query = """
        SELECT l.codigo_favorecido
        FROM liquidacoes l
        LEFT JOIN avaliacao_cnpjs a ON l.codigo_favorecido = a.cnpj
        GROUP BY l.codigo_favorecido
        HAVING COUNT(l.codigo_liquidacao) >= 3 
        AND (SUM(CASE WHEN MONTH(l.data_emissao) = 12 THEN 1 ELSE 0 END) / COUNT(l.codigo_liquidacao)) >= 0.80;
    """
    cursor.execute(query)
    return cursor.fetchall()

