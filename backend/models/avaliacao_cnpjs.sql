CREATE TABLE IF NOT EXISTS avaliacao_cnpjs (
    cnpj VARCHAR(14) PRIMARY KEY,
    
    votos_cidadaos INT DEFAULT 0
);