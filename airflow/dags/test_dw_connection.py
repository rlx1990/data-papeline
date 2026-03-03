from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG(
    dag_id="test_dw_connection",
    start_date=datetime(2026, 2, 26),
    schedule_interval=None,
    catchup=False,
    tags=["dw", "teste"],
) as dag:

    test_connection = PostgresOperator(
        task_id="test_select",
        postgres_conn_id="dw_postgres",
        sql="""
            SELECT current_database(), current_user, NOW();
        """,
    )

    test_connection