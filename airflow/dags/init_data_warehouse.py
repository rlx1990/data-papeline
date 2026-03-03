from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="init_data_warehouse",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["setup", "dw"],
) as dag:

    init_dw = PostgresOperator(
        task_id="init_dw",
        postgres_conn_id="dw_postgres_conn",
        sql="sql/init_dw.sql",
    )

    init_dw