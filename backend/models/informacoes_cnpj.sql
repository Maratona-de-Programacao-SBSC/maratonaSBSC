CREATE TABLE IF NOT EXISTS informacoes_cnpj (
    codigo_favorecido VARCHAR(14) PRIMARY KEY, 
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    cod_cnae VARCHAR(10),
    cod_natjuridica VARCHAR(10),
    tipo_pessoa VARCHAR(20),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    cep VARCHAR(8),
    bairro VARCHAR(100),
    municipio VARCHAR(100),
    uf CHAR(2),

    INDEX idx_endereco (municipio, cep, numero),
    INDEX idx_cnae (cod_cnae)
);