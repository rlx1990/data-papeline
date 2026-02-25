import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from src.config.database import get_connection


# ==========================================
# AUDITORIA
# ==========================================

def start_audit(cursor, process_name):
    cursor.execute("""
        INSERT INTO control.etl_audit_log (
            process_name,
            start_time,
            status
        )
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (process_name, datetime.now(), 'RUNNING'))

    return cursor.fetchone()[0]


def end_audit(cursor, audit_id, rows, status, error=None):
    cursor.execute("""
        UPDATE control.etl_audit_log
        SET end_time = %s,
            rows_affected = %s,
            status = %s,
            error_message = %s
        WHERE id = %s;
    """, (datetime.now(), rows, status, error, audit_id))


# ==========================================
# DIM CATEGORIA
# ==========================================

def load_dim_categoria(cursor):
    audit_id = start_audit(cursor, "dim_categoria")

    try:
        cursor.execute("""
            MERGE INTO dw.dim_categoria AS d
            USING (
                SELECT DISTINCT
                    payload->>'category' AS nome_categoria
                FROM staging.products_raw
                WHERE payload->>'category' IS NOT NULL
            ) AS s
            ON d.nome_categoria = s.nome_categoria
            WHEN NOT MATCHED THEN
                INSERT (nome_categoria)
                VALUES (s.nome_categoria);
        """)

        rows = cursor.rowcount
        end_audit(cursor, audit_id, rows, "SUCCESS")

    except Exception as e:
        end_audit(cursor, audit_id, 0, "FAILED", str(e))
        raise


# ==========================================
# DIM PRODUTO
# ==========================================

def load_dim_produto(cursor):
    audit_id = start_audit(cursor, "dim_produto")

    try:
        cursor.execute("""
            MERGE INTO dw.dim_produto AS d
            USING (
                SELECT DISTINCT ON ((pr.payload->>'id')::int)
                    (pr.payload->>'id')::int AS produto_id,
                    pr.payload->>'title' AS nome_produto,
                    (pr.payload->>'price')::numeric AS preco_base,
                    pr.payload->>'category' AS nome_categoria,
                    pr.ingestion_date
                FROM staging.products_raw pr
                ORDER BY (pr.payload->>'id')::int, pr.ingestion_date DESC
            ) AS s
            JOIN dw.dim_categoria c
                ON c.nome_categoria = s.nome_categoria
            ON d.produto_id = s.produto_id
            WHEN MATCHED THEN
                UPDATE SET
                    nome_produto = s.nome_produto,
                    preco_base = s.preco_base,
                    sk_categoria = c.sk_categoria
            WHEN NOT MATCHED THEN
                INSERT (
                    produto_id,
                    nome_produto,
                    marca,
                    preco_base,
                    sk_categoria
                )
                VALUES (
                    s.produto_id,
                    s.nome_produto,
                    NULL,
                    s.preco_base,
                    c.sk_categoria
                );
        """)

        rows = cursor.rowcount
        end_audit(cursor, audit_id, rows, "SUCCESS")

    except Exception as e:
        end_audit(cursor, audit_id, 0, "FAILED", str(e))
        raise


# ==========================================
# DIM CLIENTE
# ==========================================

def load_dim_cliente(cursor):
    audit_id = start_audit(cursor, "dim_cliente")

    try:
        cursor.execute("""
            MERGE INTO dw.dim_cliente AS d
            USING (
                SELECT DISTINCT ON ((payload->>'id')::INT)
                    (payload->>'id')::INT AS cliente_id,
                    (payload->'name'->>'firstname') || ' ' ||
                    (payload->'name'->>'lastname') AS nome_cliente,
                    payload->'address'->>'city' AS cidade,
                    payload->'address'->>'zipcode' AS estado,
                    CURRENT_DATE AS data_cadastro,
                    TRUE AS ativo
                FROM staging.users_raw
                ORDER BY (payload->>'id')::INT
            ) AS s
            ON d.cliente_id = s.cliente_id
            WHEN MATCHED THEN
                UPDATE SET
                    nome_cliente = s.nome_cliente,
                    cidade = s.cidade,
                    estado = s.estado,
                    ativo = TRUE
            WHEN NOT MATCHED THEN
                INSERT (
                    cliente_id,
                    nome_cliente,
                    cidade,
                    estado,
                    data_cadastro,
                    ativo
                )
                VALUES (
                    s.cliente_id,
                    s.nome_cliente,
                    s.cidade,
                    s.estado,
                    s.data_cadastro,
                    s.ativo
                );
        """)

        rows = cursor.rowcount
        end_audit(cursor, audit_id, rows, "SUCCESS")

    except Exception as e:
        end_audit(cursor, audit_id, 0, "FAILED", str(e))
        raise


# ==========================================
# FATO VENDAS
# ==========================================

def load_fato_vendas(cursor):
    audit_id = start_audit(cursor, "fato_vendas")

    try:
        cursor.execute("""
            SELECT last_processed_date
            FROM control.etl_metadata
            WHERE process_name = 'fato_vendas'
        """)
        last_processed_date = cursor.fetchone()[0]

        if last_processed_date is None:
            last_processed_date = '1900-01-01'

        cursor.execute("""
            WITH carts AS (
                SELECT
                    (payload->>'id')::INT AS cart_id,
                    (payload->>'userId')::INT AS user_id,
                    (payload->>'date')::TIMESTAMP AS data_venda,
                    payload->'products' AS products
                FROM staging.carts_raw
                WHERE (payload->>'date') IS NOT NULL
                  AND (payload->>'date')::TIMESTAMP > %s
            ),
            exploded AS (
                SELECT
                    c.cart_id,
                    c.user_id,
                    c.data_venda,
                    (p->>'productId')::INT AS produto_id,
                    (p->>'quantity')::INT AS quantidade
                FROM carts c
                CROSS JOIN LATERAL jsonb_array_elements(c.products) p
            )
            INSERT INTO dw.fato_vendas (
                numero_pedido,
                sk_tempo,
                sk_cliente,
                sk_produto,
                sk_categoria,
                quantidade,
                valor_unitario,
                valor_total
            )
            SELECT
                e.cart_id,
                dt.sk_tempo,
                dc.sk_cliente,
                dp.sk_produto,
                dp.sk_categoria,
                e.quantidade,
                dp.preco_base,
                e.quantidade * dp.preco_base
            FROM exploded e
            JOIN dw.dim_produto dp
                ON dp.produto_id = e.produto_id
            JOIN dw.dim_cliente dc
                ON dc.cliente_id = e.user_id
            JOIN dw.dim_tempo dt
                ON dt.data_completa = DATE(e.data_venda)
            ON CONFLICT (numero_pedido, sk_produto)
            DO NOTHING;
        """, (last_processed_date,))

        rows = cursor.rowcount

        cursor.execute("""
            UPDATE control.etl_metadata
            SET last_processed_date = COALESCE(
                (SELECT MAX((payload->>'date')::TIMESTAMP)
                 FROM staging.carts_raw),
                last_processed_date
            )
            WHERE process_name = 'fato_vendas';
        """)

        end_audit(cursor, audit_id, rows, "SUCCESS")

    except Exception as e:
        end_audit(cursor, audit_id, 0, "FAILED", str(e))
        raise


# ==========================================
# MAIN
# ==========================================

def main():
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                load_dim_categoria(cursor)
                load_dim_produto(cursor)
                load_dim_cliente(cursor)
                load_fato_vendas(cursor)
    finally:
        conn.close()


if __name__ == "__main__":
    main()