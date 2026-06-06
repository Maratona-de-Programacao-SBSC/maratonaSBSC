CREATE TABLE IF NOT EXISTS notas_fiscais (
    chave_acesso VARCHAR(44) PRIMARY KEY,
    data_emissao DATE,
    codigo_favorecido VARCHAR(14) NOT NULL,
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
    valor NUMERIC(15, 2),

    INDEX idx_codigo_favorecido (codigo_favorecido)
);

ALTER TABLE notas_fiscais 
ADD CONSTRAINT check_notas_fiscais_cnpj_nao_vazio
CHECK (LENGTH(TRIM(codigo_favorecido)) > 0 AND codigo_favorecido NOT LIKE '%*%');