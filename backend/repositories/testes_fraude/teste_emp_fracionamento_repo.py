from repositories.database import cursor, db

def busca_empenhos_fracionados() -> list:
    """
    Busca CNPJs que possuem 2 ou mais empenhos com valores muito próximos
    aos tetos legais de dispensa de licitação (Lei 14.133/2021).
    Foca na zona de risco: 90% a 100% do teto atualizado.
    """
    query = """
        SELECT 
            e.codigo_favorecido AS cnpj,
            COUNT(e.codigo_empenho) AS qtd_empenhos,
            SUM(e.valor) AS valor_total_suspeito
        FROM empenhos e
        LEFT JOIN auditoria_cnpjs a ON e.codigo_favorecido = a.cnpj
        WHERE e.codigo_favorecido IS NOT NULL
          AND (a.teste_fracionamento_empenho IS NULL OR a.teste_fracionamento_empenho = 0)
          AND (
              -- Zona de Risco 1: Compras e Serviços (Teto ~ R$ 59.906,02)
              (e.valor BETWEEN 53900.00 AND 59906.02)
              OR 
              -- Zona de Risco 2: Obras e Engenharia (Teto ~ R$ 119.812,02)
              (e.valor BETWEEN 107800.00 AND 119812.02)
          )
        GROUP BY e.codigo_favorecido
        -- Só é crime de fracionamento se houver recorrência (2 ou mais empenhos)
        HAVING COUNT(e.codigo_empenho) >= 2
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela de auditoria ou atualiza o score se ele já existir.
    """
    query = """
        INSERT INTO auditoria_cnpjs (
            cnpj, teste_fracionamento_empenho, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_fracionamento_empenho = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()