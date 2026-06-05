from repositories.database import cursor, db

def busca_sedes_compartilhadas() -> list:
    """
    Busca CNPJs que dividem exatamente o mesmo endereço físico (CEP + Número).
    Ignora endereços 'Sem Número' (S/N) para evitar falsos positivos em áreas rurais.
    """
    query = """
        SELECT 
            c.codigo_favorecido AS cnpj,
            c.razao_social,
            c.logradouro,
            c.numero,
            c.cep,
            shared.qtd_empresas
        FROM informacoes_cnpj c
        -- Subconsulta que mapeia os endereços com superlotação de CNPJs
        INNER JOIN (
            SELECT cep, numero, COUNT(codigo_favorecido) AS qtd_empresas
            FROM informacoes_cnpj
            WHERE cep IS NOT NULL AND cep != ''
              AND numero IS NOT NULL AND numero != ''
              AND UPPER(numero) NOT IN ('S/N', 'SN', '0')
            GROUP BY cep, numero
            HAVING COUNT(codigo_favorecido) > 1
        ) shared ON c.cep = shared.cep AND c.numero = shared.numero
        LEFT JOIN avaliacao_cnpjs a ON c.codigo_favorecido = a.cnpj
        WHERE (a.teste_sede_fantasma IS NULL OR a.teste_sede_fantasma = 0)
    """
    cursor.execute(query)
    return cursor.fetchall()

def salva_falha(cnpj: str):
    """
    Insere o CNPJ na tabela de auditoria ou atualiza o score se ele já existir.
    """
    query = """
        INSERT INTO avaliacao_cnpjs (
            cnpj, teste_sede_fantasma, score_automatico, score_total, data_ultima_auditoria
        ) VALUES (
            %(cnpj)s, 1, 1, 1, CURRENT_DATE()
        )
        ON DUPLICATE KEY UPDATE
            teste_sede_fantasma = 1,
            score_automatico = score_automatico + 1,
            score_total = score_total + 1,
            data_ultima_auditoria = CURRENT_DATE()
    """
    cursor.execute(query, {"cnpj": cnpj})
    db.commit()