from repositories.database import cursor, db

def busca_sedes_compartilhadas() -> list:
    """
    Busca CNPJs que dividem exatamente o mesmo endereço físico (CEP + Número).
    Ignora endereços 'Sem Número' (S/N) para evitar falsos positivos em áreas rurais.
    """
    query = """
        WITH contagem AS (
            SELECT cep, numero, municipio, complemento, bairro, cod_cnae,
                COUNT(*) AS quantidade_cnae,
                SUM(COUNT(*)) OVER (PARTITION BY cep, numero, municipio, complemento, bairro) AS total_local
            FROM informacoes_cnpj
            GROUP BY cep, numero, municipio, complemento, bairro, cod_cnae
        ),
        grupos_fraude AS (
            SELECT cep, numero, municipio, complemento, bairro, cod_cnae
            FROM contagem
            WHERE (quantidade_cnae / total_local) > 0.85
            AND total_local > 50
        )
        SELECT i.codigo_favorecido
        FROM informacoes_cnpj i
        JOIN grupos_fraude gf
        ON i.cep = gf.cep
        AND i.numero = gf.numero
        AND i.municipio = gf.municipio
        AND i.cod_cnae = gf.cod_cnae
        AND IFNULL(i.complemento, '') = IFNULL(gf.complemento, '')
        AND IFNULL(i.bairro, '') = IFNULL(gf.bairro, '')
    """
    cursor.execute(query)
    return cursor.fetchall()



