CREATE TABLE IF NOT EXISTS avaliacao_cnpjs (
    cnpj VARCHAR(14) PRIMARY KEY,
    
    votos_cidadaos INT DEFAULT 0,   -- O "+1" que o usuário der no Front-end
    score_total INT DEFAULT 0,      -- (score_automatico + votos_cidadaos)
    
);