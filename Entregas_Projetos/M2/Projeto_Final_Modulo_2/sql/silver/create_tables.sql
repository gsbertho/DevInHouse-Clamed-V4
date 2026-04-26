CREATE SCHEMA IF NOT EXISTS silver;

-- =========================
-- DIM_FILIAL
-- =========================
CREATE TABLE IF NOT EXISTS silver.dim_filial (
    filial_id TEXT PRIMARY KEY,
    brick TEXT,
    regiao TEXT,
    cluster TEXT
);

-- =========================
-- DIM_PRODUTO
-- =========================
CREATE TABLE IF NOT EXISTS silver.dim_produto (
    produto_id TEXT PRIMARY KEY,
    categoria TEXT,
    nome_produto TEXT
);

-- =========================
-- FATO_VENDAS
-- =========================
CREATE TABLE IF NOT EXISTS silver.fato_vendas (
    data DATE,
    produto_id TEXT,
    filial_id TEXT,
    empresa TEXT,
    volume INTEGER,
    preco_unitario NUMERIC,
    receita NUMERIC,

    FOREIGN KEY (produto_id) REFERENCES silver.dim_produto(produto_id),
    FOREIGN KEY (filial_id) REFERENCES silver.dim_filial(filial_id)
);