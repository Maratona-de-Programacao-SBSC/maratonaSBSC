from repositories.database import cursor, db

def busca_pagamentos_sem_empenho() -> list:
    """
    Busca CNPJs/CPFs que estão na tabela de pagamentos, mas NÃO possuem empenho.
    Filtro aprimorado para ignorar CPFs anonimizados (***) e códigos internos.
    """
    query = """
        SELECT DISTINCT p.codigo_favorecido AS cnpj
        FROM pagamentos p
        LEFT JOIN empenhos e ON p.codigo_favorecido = e.codigo_favorecido
        LEFT JOIN avaliacao_cnpjs a ON p.codigo_favorecido = a.cnpj
        WHERE e.codigo_favorecido IS NULL
          AND p.codigo_favorecido IS NOT NULL
          
          -- FILTRO CARACTER: Garante que a string contenha APENAS NÚMEROS (ignora *, -, letras)
          AND p.codigo_favorecido REGEXP '^[0-9]+$'
          
          -- FILTRO DE TAMANHO: Garante que seja exatamente um CPF (11) ou CNPJ (14)
          AND LENGTH(p.codigo_favorecido) IN (11, 14)
          
          AND (a.teste_pagamento_sem_empenho IS NULL OR a.teste_pagamento_sem_empenho = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela avaliacao_cnpjs.
    """
    query = """
        INSERT INTO avaliacao_cnpjs (
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