from repositories.database import cursor, db

def busca_pagamentos_fim_de_semana() -> list:
    """
    Busca CNPJs/CPFs que receberam pagamentos no sábado ou domingo.
    No MySQL, DAYOFWEEK() retorna 1 para Domingo e 7 para Sábado.
    """
    query = """
        SELECT DISTINCT p.codigo_favorecido AS cnpj
        FROM pagamentos p
        LEFT JOIN avaliacao_cnpjs a ON p.codigo_favorecido = a.cnpj
        WHERE DAYOFWEEK(p.data_emissao) IN (1, 7)
          AND p.codigo_favorecido IS NOT NULL
          -- Filtro de limpeza: Garante que seja um CPF (11) ou CNPJ (14) apenas numérico
          AND p.codigo_favorecido REGEXP '^[0-9]+$'
          AND LENGTH(p.codigo_favorecido) IN (11, 14)
          -- Garante que não vamos testar quem já foi pego neste critério
          AND (a.teste_pagamento_fim_de_semana IS NULL OR a.teste_pagamento_fim_de_semana = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela avaliacao_cnpjs, marcando a falha de fim de semana.
    """
    query = """
        INSERT INTO avaliacao_cnpjs (
            cnpj, teste_pagamento_fim_de_semana, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_pagamento_fim_de_semana = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()