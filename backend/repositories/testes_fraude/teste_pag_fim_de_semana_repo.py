from repositories.database import cursor, db

def busca_pagamentos_fim_de_semana() -> list:
    """
    Busca CNPJs que receberam pagamentos aos finais de semana.
    Filtro SQL: DAYOFWEEK() retorna 1 para Domingo e 7 para Sábado.
    Ignora CNPJs que já falharam neste teste específico.
    """
    query = """
        SELECT DISTINCT p.codigo_favorecido AS cnpj
        FROM pagamentos p
        LEFT JOIN auditoria_cnpjs a ON p.codigo_favorecido = a.cnpj
        WHERE DAYOFWEEK(p.data_emissao) IN (1, 7)
          AND p.codigo_favorecido IS NOT NULL
          AND (a.teste_pagamentos_fim_de_semana IS NULL OR a.teste_pagamentos_fim_de_semana = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela de auditoria ou atualiza o score se ele já existir.
    """
    query = """
        INSERT INTO auditoria_cnpjs (
            cnpj, teste_pagamentos_fim_de_semana, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_pagamentos_fim_de_semana = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()