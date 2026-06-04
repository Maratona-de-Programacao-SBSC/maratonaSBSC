from repositories.database import cursor, db

def busca_pagamentos_sem_empenho() -> list:
    """
    Busca CNPJs que estão na tabela de pagamentos, 
    mas NÃO possuem nenhum registro correspondente na tabela de empenhos.
    """
    query = """
        SELECT DISTINCT p.codigo_favorecido AS cnpj
        FROM pagamentos p
        -- Tenta cruzar com os empenhos pelo CNPJ
        LEFT JOIN empenhos e ON p.codigo_favorecido = e.codigo_favorecido
        -- Traz a auditoria para não testar quem já falhou
        LEFT JOIN auditoria_cnpjs a ON p.codigo_favorecido = a.cnpj
        -- O 'pulo do gato': Se o lado do empenho for NULO, significa que o pagamento não tem empenho!
        WHERE e.codigo_favorecido IS NULL
          AND p.codigo_favorecido IS NOT NULL
          AND (a.teste_pagamento_sem_empenho IS NULL OR a.teste_pagamento_sem_empenho = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela de auditoria ou atualiza o score se ele já existir.
    """
    query = """
        INSERT INTO auditoria_cnpjs (
            cnpj, teste_pagamento_sem_empenho, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_pagamento_sem_empenho = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()