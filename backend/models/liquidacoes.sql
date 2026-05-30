CREATE TABLE IF NOT EXISTS liquidacoes (
    codigo_liquidacao VARCHAR(50) PRIMARY KEY,
    data_emissao DATE,
    codigo_orgao INTEGER,
    codigo_unidade_gestora INTEGER,
    codigo_favorecido VARCHAR(14),
    favorecido VARCHAR(200),
    observacao VARCHAR(200),
    codigo_elemento_despesa VARCHAR(10)
);