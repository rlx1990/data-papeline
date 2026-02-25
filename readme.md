>>       Data Pipeline & Data Warehouse 

Pipeline completo de Engenharia de Dados com ingestão de API pública, modelagem dimensional, carga incremental, auditoria de execução e orquestração com Apache Airflow.

>>Objetivo

Simular um ambiente corporativo de dados, contemplando:

Ingestão de dados via API

Armazenamento em camada Staging (JSON raw)

Transformação para Data Warehouse dimensional (Star Schema)

Carga incremental controlada por metadata

Auditoria de execução de ETL

Orquestração com Apache Airflow

Ambiente containerizado com Docker

>> Boas Práticas Aplicadas 

Separação de camadas (Staging / DW)

Idempotência com ON CONFLICT

Controle incremental via metadata

Auditoria de execução

Uso de MERGE

Tratamento de exceções

Organização modular do código

Containerização

Arquitetura

>> Fluxo do pipeline:

API → Staging (raw JSON) → Transformação → Data Warehouse → Airflow

Camadas implementadas:

Staging: armazenamento bruto em JSONB

Data Warehouse: modelo estrela com dimensões e fato

Orquestração: DAG no Airflow com dependências entre tarefas

>> Stack Utilizada

Python

PostgreSQL

Apache Airflow

Docker / Docker Compose

Psycopg2

SQL (PostgreSQL)

Modelagem Dimensional

Esquema estrela composto por:

>> Dimensões

dim_categoria

dim_produto

dim_cliente

dim_tempo

>> Fato

fato_vendas

A tabela fato possui constraint única composta:

(numero_pedido, sk_produto)

Garantindo idempotência e prevenindo duplicidade.

Carga Incremental

A carga da fato é incremental com base na tabela:

control.etl_metadata

O campo last_processed_date define o ponto de corte para novas execuções.

>> Benefícios:

Evita reprocessamento completo

Permite execução recorrente segura

Reduz custo computacional

Auditoria de ETL

Cada processo registra:

Nome do processo

Horário de início e fim

Quantidade de linhas afetadas

Status (SUCCESS / FAILED)

Mensagem de erro

Tabela utilizada:

control.etl_audit_log

Isso permite rastreabilidade e observabilidade do pipeline.

>> Orquestração

O pipeline é orquestrado via Apache Airflow com tasks independentes:

dim_categoria → dim_produto → fato_vendas
dim_cliente → fato_vendas

Executado com PythonOperator, respeitando dependências entre dimensões e fato.

>> Execução

Execução manual:

python -m src.transformation.transform

Execução via Docker (Airflow):

cd airflow
docker-compose up --build

Acesso:

http://localhost:8080

Boas Práticas Aplicadas

Separação de camadas (Staging / DW)

Idempotência com ON CONFLICT

Controle incremental via metadata

Auditoria de execução

Uso de MERGE

Tratamento de exceções

Organização modular do código

Containerização