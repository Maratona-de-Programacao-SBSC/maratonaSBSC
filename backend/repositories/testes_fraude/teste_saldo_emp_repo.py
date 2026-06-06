from repositories.database import cursor, db

def busca_cnpjs_com_saldo_estourado() -> list:
    """
    Verifica se existe alugum empenho em 6 meses que possua valor maior igual a pagamento
    """
    query = """
        SELECT 
            p.codigo_favorecido,
            p.favorecido,
            SUM(p.valor) AS total_pago,
            COALESCE(e.total_empenhado, 0) AS total_empenhado,
            (SUM(p.valor) - COALESCE(e.total_empenhado, 0)) AS valor_excedente
        FROM pagamentos p
        LEFT JOIN (
            SELECT codigo_favorecido, SUM(valor) AS total_empenhado
            FROM empenhos
            GROUP BY codigo_favorecido
        ) e ON p.codigo_favorecido = e.codigo_favorecido
        GROUP BY p.codigo_favorecido, p.favorecido, e.total_empenhado
        HAVING SUM(p.valor) > COALESCE(e.total_empenhado, 0)
        ORDER BY valor_excedente DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()

