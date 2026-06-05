from repositories.database import cursor, db

def busca_cnpjs_com_saldo_estourado() -> list:
    """
    Verifica se existe alugum empenho em 6 meses que possua valor maior igual a pagamento
    """
    query = """
        SELECT DISTINCT
            p.codigo_favorecido
        FROM pagamentos p
        JOIN empenhos e 
            ON p.codigo_favorecido = e.codigo_favorecido
            AND e.data_emissao BETWEEN DATE_SUB(p.data_emissao, INTERVAL 6 MONTH) AND p.data_emissao
        WHERE p.valor > 0
        GROUP BY p.codigo_pagamento, p.codigo_favorecido, p.data_emissao, p.valor
        HAVING p.valor > SUM(e.valor);
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