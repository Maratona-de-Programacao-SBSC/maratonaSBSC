from repositories.database import cursor, db

def busca_cnpjs_com_saldo_estourado() -> list:
    """
    Busca CNPJs onde o somatório de pagamentos supera o total empenhado.
    """
    query = """
        SELECT 
            p_total.cnpj,
            p_total.total_pago,
            e_total.total_empenhado
        FROM (
            SELECT codigo_favorecido AS cnpj, SUM(valor) AS total_pago
            FROM pagamentos
            WHERE codigo_favorecido IS NOT NULL
              AND codigo_favorecido REGEXP '^[0-9]+$'
            GROUP BY codigo_favorecido
        ) p_total
        INNER JOIN (
            SELECT codigo_favorecido AS cnpj, SUM(valor) AS total_empenhado
            FROM empenhos
            WHERE codigo_favorecido IS NOT NULL
            GROUP BY codigo_favorecido
        ) e_total ON p_total.cnpj = e_total.cnpj
        LEFT JOIN avaliacao_cnpjs a ON p_total.cnpj = a.cnpj
        WHERE p_total.total_pago > e_total.total_empenhado
          AND (a.teste_saldo_empenho IS NULL OR a.teste_saldo_empenho = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Atualiza o score na tabela de avaliacao_cnpjs.
    """
    query = """
        INSERT INTO avaliacao_cnpjs (
            cnpj, teste_saldo_empenho, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_saldo_empenho = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()