from repositories.database import cursor, db

def busca_cnpjs_com_saldo_estourado() -> list:
    """
    Busca CNPJs onde o somatório de todos os pagamentos recebidos
    é maior do que o somatório de todos os empenhos emitidos para ele.
    """
    query = """
        SELECT 
            p_total.cnpj,
            p_total.total_pago,
            e_total.total_empenhado
        FROM (
            -- Subconsulta: Total pago por CNPJ
            SELECT codigo_favorecido AS cnpj, SUM(valor) AS total_pago
            FROM pagamentos
            WHERE codigo_favorecido IS NOT NULL
            GROUP BY codigo_favorecido
        ) p_total
        INNER JOIN (
            -- Subconsulta: Total empenhado por CNPJ
            SELECT codigo_favorecido AS cnpj, SUM(valor) AS total_empenhado
            FROM empenhos
            WHERE codigo_favorecido IS NOT NULL
            GROUP BY codigo_favorecido
        ) e_total ON p_total.cnpj = e_total.cnpj
        LEFT JOIN auditoria_cnpjs a ON p_total.cnpj = a.cnpj
        -- O Filtro implacável: Recebeu mais do que tinha de direito empenhado
        WHERE p_total.total_pago > e_total.total_empenhado
          AND (a.teste_saldo_empenho IS NULL OR a.teste_saldo_empenho = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela de auditoria ou atualiza o score se ele já existir.
    """
    query = """
        INSERT INTO auditoria_cnpjs (
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