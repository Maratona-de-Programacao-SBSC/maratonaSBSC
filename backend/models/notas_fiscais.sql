CREATE TABLE IF NOT EXISTS notas_fiscais (
    chave_acesso VARCHAR(44) PRIMARY KEY,
    data_emissao DATE,
    cpf_cnpj_emitente VARCHAR(14),
    razao_social_emitente VARCHAR(200),
    uf_emitente CHAR(2),
    municipio_emitente VARCHAR(100),
    codigo_orgao_destinatario INTEGER,
    orgao_destinatario VARCHAR(200),
    cnpj_destinatario VARCHAR(14),
    nome_destinatario VARCHAR(200),
    uf_destinatario CHAR(2),
    destino_operacao SMALLINT,
    consumidor_final SMALLINT,
    valor NUMERIC(15, 2)
);