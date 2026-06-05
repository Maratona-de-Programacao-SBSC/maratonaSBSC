from repositories.database import cursor, db

def busca_sedes_compartilhadas() -> list:
    """
    Busca CNPJs que dividem exatamente o mesmo endereço físico (CEP + Número).
    Ignora endereços 'Sem Número' (S/N) para evitar falsos positivos em áreas rurais.
    """
    query = """
        WITH calculo_total_empresas AS (
            SELECT cep, numero, municipio, complemento, bairro,
            COUNT(*) as total_local
            FROM informacoes_cnpj
            GROUP BY cep, numero, municipio, complemento, bairro
        ),
        contagemCnae AS (
            SELECT cep, numero, municipio, cod_cnae, complemento, bairro,
            COUNT(*) as quantidade_cnae
            FROM informacoes_cnpj
            GROUP BY cep, numero, municipio, cod_cnae, complemento, bairro
        ),
        grupos_fraude AS (
            SELECT cc.cep, cc.numero, cc.municipio, cc.cod_cnae, cc.complemento, cc.bairro
            FROM contagemCnae cc
            JOIN calculo_total_empresas ct 
              ON cc.cep = ct.cep 
              AND cc.numero = ct.numero 
              AND cc.municipio = ct.municipio
              AND IFNULL(cc.complemento, '') = IFNULL(ct.complemento, '')
              AND IFNULL(cc.bairro, '') = IFNULL(ct.bairro, '')
            WHERE (cc.quantidade_cnae / ct.total_local) > 0.85
              AND ct.total_local > 50
        )
        SELECT 
            i.codigo_favorecido
        FROM informacoes_cnpj i
        JOIN grupos_fraude gf 
          ON i.cep = gf.cep 
          AND i.numero = gf.numero 
          AND i.municipio = gf.municipio 
          AND i.cod_cnae = gf.cod_cnae
          AND IFNULL(i.complemento, '') = IFNULL(gf.complemento, '')
          AND IFNULL(i.bairro, '') = IFNULL(gf.bairro, '');
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