CREATE TABLE IF NOT EXISTS empenhos (
    codigo_empenho VARCHAR(50) PRIMARY KEY,
    id_empenho BIGINT,
    data_emissao DATE,
    tipo_empenho VARCHAR(50),
    codigo_orgao INTEGER,
    codigo_unidade_gestora INTEGER,
    codigo_favorecido VARCHAR(14),
    favorecido VARCHAR(200),
    observacao TEXT,
    elemento_despesa VARCHAR(20),
    valor NUMERIC(15, 2),

    INDEX idx_codigo_favorecido (codigo_favorecido)
);