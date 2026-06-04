CREATE TABLE IF NOT EXISTS auditoria_cnpjs (
    cnpj VARCHAR(14) PRIMARY KEY,
    
    -- ==========================================
    -- TESTES AUTOMÁTICOS (Booleanos: 1 para Falhou/Suspeito, 0 para Passou)
    -- ==========================================
    teste_idade_empresa TINYINT(1) DEFAULT 0,  -- Antigo Gatekeeper
    -- teste_valores_incompativeis TINYINT(1) DEFAULT 0, (Adicionaremos no futuro)
    -- teste_pagamento_sem_empenho TINYINT(1) DEFAULT 0, (Adicionaremos no futuro)
    teste_pagamento_fim_de_semana TINYINT(1) DEFAULT 0
    
    -- ==========================================
    -- SISTEMA DE PONTUAÇÃO (Score)
    -- ==========================================
    score_automatico INT DEFAULT 0, -- Soma dos testes automáticos que falharam
    votos_cidadaos INT DEFAULT 0,   -- O "+1" que o usuário der no Front-end
    score_total INT DEFAULT 0,      -- (score_automatico + votos_cidadaos)
    
    -- ==========================================
    -- CONTROLE
    -- ==========================================
    data_ultima_auditoria DATE
);