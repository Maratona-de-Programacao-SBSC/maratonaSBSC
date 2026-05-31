CREATE TABLE IF EXISTS pagamentos (
    codigo_pagamento VARCHAR(50) PRIMARY KEY,
    data_emissao DATE,
    codigo_favorecido VARCHAR(14),
    favorecido VARCHAR(200),
    processo VARCHAR(50),
    codigo_unidade_gestora INTEGER,
    unidade_gestora VARCHAR(200),
    codigo_orgao INTEGER,
    orgao VARCHAR(200),
    observacao VARCHAR(200),
    valor NUMERIC(15, 2)
);