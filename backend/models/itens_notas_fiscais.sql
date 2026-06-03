CREATE TABLE itens_notas_fiscais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chave_nota VARCHAR(44),
    numero_produto VARCHAR(10),
    descricao VARCHAR(500),
    codigo_ncm VARCHAR(10),
    ncm VARCHAR(200),
    cfop VARCHAR(10),
    quantidade NUMERIC(15,4),
    unidade VARCHAR(10),
    valor_unitario NUMERIC(15,4),
    valor NUMERIC(15,2),
    FOREIGN KEY (chave_nota) REFERENCES notas_fiscais(chave_acesso)
);