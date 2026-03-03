
CREATE SCHEMA IF NOT EXISTS control;
CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE IF NOT EXISTS control.etl_audit_log (
    id SERIAL PRIMARY KEY,
    process_name VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),
    rows_affected INTEGER,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS control.etl_metadata (
    process_name VARCHAR(100) PRIMARY KEY,
    last_processed_date TIMESTAMP
);

INSERT INTO control.etl_metadata (process_name, last_processed_date)
VALUES ('fato_vendas', '1900-01-01')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS dw.dim_categoria (
    sk_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS dw.dim_produto (
    sk_produto SERIAL PRIMARY KEY,
    produto_id INT UNIQUE,
    nome_produto VARCHAR(255),
    marca VARCHAR(100),
    preco_base NUMERIC,
    sk_categoria INT REFERENCES dw.dim_categoria(sk_categoria)
);

CREATE TABLE IF NOT EXISTS dw.dim_cliente (
    sk_cliente SERIAL PRIMARY KEY,
    cliente_id INT UNIQUE,
    nome_cliente VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    data_cadastro DATE,
    ativo BOOLEAN
);

CREATE TABLE IF NOT EXISTS dw.dim_tempo (
    sk_tempo SERIAL PRIMARY KEY,
    data_completa DATE UNIQUE
);

INSERT INTO dw.dim_tempo (data_completa)
SELECT generate_series('2020-01-01'::date, '2030-12-31', '1 day')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS dw.fato_vendas (
    sk_venda SERIAL PRIMARY KEY,
    numero_pedido INT,
    sk_tempo INT REFERENCES dw.dim_tempo(sk_tempo),
    sk_cliente INT REFERENCES dw.dim_cliente(sk_cliente),
    sk_produto INT REFERENCES dw.dim_produto(sk_produto),
    sk_categoria INT,
    quantidade INT,
    valor_unitario NUMERIC,
    valor_total NUMERIC,
    UNIQUE (numero_pedido, sk_produto)
);