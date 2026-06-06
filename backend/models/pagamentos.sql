CREATE TABLE IF NOT EXISTS pagamentos (
    codigo_pagamento VARCHAR(50) PRIMARY KEY,
    data_emissao DATE,
    codigo_favorecido VARCHAR(14) NOT NULL,
    favorecido VARCHAR(200),
    processo VARCHAR(50),
    codigo_unidade_gestora INTEGER,
    unidade_gestora VARCHAR(200),
    codigo_orgao INTEGER,
    orgao VARCHAR(200),
    observacao TEXT,
    valor NUMERIC(15, 2),

    INDEX idx_codigo_favorecido (codigo_favorecido)
);