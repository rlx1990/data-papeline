# 🚀 Data Pipeline & Data Warehouse

Este projeto simula um **pipeline de dados corporativo completo**, incluindo ingestão de API, armazenamento em Data Lake, processamento distribuído com Spark, modelagem dimensional em Data Warehouse, carga incremental, auditoria de execução e orquestração com Airflow.

Todo o ambiente é **containerizado com Docker**, garantindo isolamento de dependências, reprodutibilidade e facilidade de execução em qualquer máquina.

---

# 📚 Sumário

* [Visão Geral](#-visão-geral)
* [Arquitetura](#-arquitetura)
* [Fluxo de Dados](#-fluxo-de-dados)
* [Camadas de Dados](#-camadas-de-dados)
* [Modelagem Dimensional](#-modelagem-dimensional)
* [Carga Incremental](#-carga-incremental)
* [Auditoria](#-auditoria)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Stack Tecnológica](#-stack-tecnológica)
* [Execução com Docker](#-execução-com-docker)

---

# 📊 Visão Geral

O projeto simula um ambiente de **Engenharia de Dados moderno**, contemplando:

* Ingestão de dados via API pública
* Armazenamento em Data Lake (Raw/Bronze)
* Processamento distribuído com Spark
* Transformação e padronização dos dados
* Modelagem dimensional em Data Warehouse
* Carga incremental controlada
* Auditoria de execução
* Orquestração de pipelines com Airflow

---

# 🏗 Arquitetura

O pipeline segue a arquitetura **Data Lake + Data Warehouse**:

```
API
 │
 ▼
Raw Layer (JSON)
 │
 ▼
Spark Processing
 │
 ▼
Silver Layer
 │
 ▼
Data Warehouse (PostgreSQL)
 │
 ▼
Analytics / BI
```

Componentes principais:

* **API Source** – origem dos dados
* **Data Lake** – armazenamento bruto
* **Spark** – processamento distribuído
* **PostgreSQL** – Data Warehouse
* **Airflow** – orquestração

---

# 🔄 Fluxo de Dados

## 1️⃣ Ingestão

Coleta de dados da **FakeStore API**.

Entidades extraídas:

* Products
* Users
* Carts

Os dados são armazenados em **JSON na camada Raw**.

---

## 2️⃣ Camada Raw (Bronze)

Características:

* Dados **sem transformação**
* Armazenamento em formato JSON
* Organização por data de ingestão
* Permite **reprocessamento completo**

---

## 3️⃣ Processamento com Spark

O **Apache Spark** é utilizado para:

* Leitura dos dados da camada Raw
* Limpeza e padronização
* Conversão de tipos
* Normalização dos dados
* Preparação para carga analítica

Essa etapa gera a **camada Silver**.


## 4️⃣ Camada Silver

Nesta camada os dados já estão:

* Estruturados
* Limpos
* Padronizados
* Prontos para modelagem analítica

---

## 5️⃣ Data Warehouse

Os dados processados são carregados em um **Data Warehouse PostgreSQL**, utilizando modelagem dimensional.

---

# 🧱 Camadas de Dados

O projeto segue o padrão **Medallion Architecture**:

| Camada     | Descrição                         |
| ---------- | --------------------------------- |
| **Bronze** | Dados brutos da API               |
| **Silver** | Dados tratados com Spark          |
| **Gold**   | Dados modelados no Data Warehouse |

---

# ⭐ Modelagem Dimensional

O Data Warehouse segue o padrão **Star Schema**.

## Dimensões

* `dim_product`
* `dim_user`
* `dim_date`

Características:

* Dados descritivos
* Uso de **Surrogate Keys**
* Preparado para evolução futura

---

## Tabela Fato

`fact_sales`

Contém métricas quantitativas e relacionamentos com dimensões.

Exemplo estrutural:

```
fact_sales
-----------
id
product_key
user_key
date_key
quantity
price
total_amount
```

---

# 🔁 Carga Incremental

O pipeline implementa estratégia de controle de execução.

Funcionalidades:

* Controle de execução por auditoria
* Evita reprocessamento desnecessário
* Preparado para expansão futura
* Controle por timestamp
* Controle por ID máximo

---

# 🧾 Auditoria

Tabela: `etl_audit_log`

| Campo          | Descrição             |
| -------------- | --------------------- |
| process_name   | Nome do processo      |
| start_time     | Início da execução    |
| end_time       | Fim da execução       |
| status         | Sucesso / Falha       |
| rows_processed | Quantidade processada |
| error_message  | Mensagem de erro      |

Objetivo:

* Monitoramento
* Observabilidade
* Governança de dados

---

# 📂 Estrutura do Projeto

```
data-pipeline
│
├── airflow
│   ├── dags
│   └── logs
│
├── src
│   ├── ingestion
│   │   └── api_ingestion.py
│   │
│   ├── spark
│   │   └── bronze_to_silver.py
│   │
│   ├── warehouse
│   │   └── load_dw.py
│   │
│   └── data
│       ├── raw
│       └── silver
│
├── sql
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🧰 Stack Tecnológica

| Tecnologia     | Finalidade                |
| -------------- | ------------------------- |
| Python         | Ingestão e transformação  |
| Apache Spark   | Processamento distribuído |
| PostgreSQL     | Data Warehouse            |
| Apache Airflow | Orquestração de pipelines |
| Docker         | Containerização           |
| SQL            | Modelagem e consultas     |
| Git            | Versionamento             |

---

# 🐳 Execução com Docker

Todo o ambiente é executado via Docker.

Serviços disponíveis:

* **Spark Master**
* **Spark Worker**
* **PostgreSQL (DW)**
* **PostgreSQL (Airflow Metadata)**
* **Airflow Scheduler**
* **Airflow Webserver**

# Subir ambiente

docker-compose up -d

# Interfaces

* Airflow:http://localhost:8080



