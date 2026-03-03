from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="pipeline_orchestrator",
    start_date=datetime(2026, 2, 26),
    schedule_interval=None,
    catchup=False,
    tags=["pipeline", "dw"],
) as dag:

    ingest_api = BashOperator(
        task_id="ingest_api",
        bash_command="cd /opt/airflow && python -m src.ingestion.ingest_api"
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="cd /opt/airflow && python -m src.transformation.transform"
    )

    ingest_api >> transform