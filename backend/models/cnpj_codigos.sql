

CREATE TABLE IF NOT EXISTS cnpj_codigos(
    codigo_favorecido VARCHAR(140),
    codigo VARCHAR(100),
    tipo VARCHAR(100),
    
    PRIMARY KEY (codigo_favorecido, codigo, tipo)
)


