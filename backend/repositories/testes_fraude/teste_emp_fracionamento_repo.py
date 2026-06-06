from repositories.database import cursor, db

def busca_empenhos_fracionados(ano: int) -> list:
    """
    Busca CNPJs com empenhos fracionados filtrando pelo ano do exercício.
    """
    query = """
        SELECT 
            e.codigo_favorecido AS cnpj,
            COUNT(e.codigo_empenho) AS qtd_empenhos,
            SUM(e.valor) AS valor_total_suspeito
        FROM empenhos e
        LEFT JOIN avaliacao_cnpjs a ON e.codigo_favorecido = a.cnpj
        WHERE e.codigo_favorecido IS NOT NULL
          AND e.codigo_favorecido REGEXP '^[0-9]+$'
          AND LENGTH(e.codigo_favorecido) = 14
          -- Filtro de Ano
          AND YEAR(e.data_emissao) = %(ano)s
          AND (a.teste_fracionamento_empenho IS NULL OR a.teste_fracionamento_empenho = 0)
          AND (
              (e.valor BETWEEN 53900.00 AND 59906.02)
              OR 
              (e.valor BETWEEN 107800.00 AND 119812.02)
          )
        GROUP BY e.codigo_favorecido
        HAVING COUNT(e.codigo_empenho) >= 2
    """
    cursor.execute(query, {'ano': ano})
    return cursor.fetchall()

