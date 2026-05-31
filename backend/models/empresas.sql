CREATE TABLE IF NOT EXISTS empresas (
    codigo_favorecido VARCHAR(14) PRIMARY KEY,
    razao_social VARCHAR(200),
    data_criacao DATE,
    localizacao VARCHAR(200)
);