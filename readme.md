#  Data Pipeline & Data Warehouse

Projeto de Engenharia de Dados que simula um ambiente corporativo completo, incluindo ingestão de API, armazenamento em camada Raw, transformação para Data Warehouse dimensional, carga incremental, auditoria e orquestração com Airflow.

---

#  Sumário

* [Visão Geral](#-visão-geral)
* [Arquitetura](#-arquitetura)
* [Fluxo de Dados](#-fluxo-de-dados)
* [Modelagem Dimensional](#-modelagem-dimensional)
* [Carga Incremental](#-carga-incremental)
* [Auditoria](#-auditoria)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Stack Tecnológica](#-stack-tecnológica)
* [Possibilidades Analíticas](#-possibilidades-analíticas)
* [Evoluções Futuras](#-evoluções-futuras)

---

#  Visão Geral

Este projeto foi desenvolvido com o objetivo de simular um pipeline de dados corporativo, contemplando:

* Ingestão de dados via API pública
* Armazenamento de dados brutos (Raw Layer)
* Transformação e modelagem dimensional
* Carga incremental controlada
* Auditoria de execução
* Orquestração com Airflow

---

#  Arquitetura

A arquitetura segue um padrão clássico de Data Warehouse:

```
API → Camada Raw (JSON) → Transformação → Data Warehouse (Postgres) → Consultas Analíticas
```

Camadas:

1. Ingestão
2. Raw
3. Transformação
4. Data Warehouse
5. Camada Analítica

---

#  Fluxo de Dados

## 1️ Ingestão

* Consumo da API FakeStore
* Extração de:

  * Products
  * Users
  * Carts
* Salvamento em JSON na camada Raw

## 2️ Camada Raw

* Dados armazenados sem transformação
* Organização por data de extração
* Base para reprocessamento futuro

## 3️ Transformação

* Limpeza e padronização
* Conversão de tipos
* Tratamento de nulos
* Separação em dimensões e fatos

## 4️ Data Warehouse

* Modelo dimensional (Star Schema)
* Separação entre tabelas fato e dimensão
* Uso de surrogate keys

---

#  Modelagem Dimensional

O projeto utiliza o padrão **Star Schema**, separando:

##  Dimensões

* `dim_product`
* `dim_user`
* `dim_date`

Características:

* Dados descritivos
* Identificador substituto (Surrogate Key)
* Preparado para evolução (SCD)

##  Tabela Fato

* `fact_sales`
* Contém métricas quantitativas
* Chaves estrangeiras para dimensões

Exemplo estrutural:

```sql
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

#  Carga Incremental

O pipeline implementa estratégia de controle de execução:

* Registro de execução via auditoria
* Evita reprocessamento desnecessário
* Preparado para:

  * Controle por timestamp
  * Controle por ID máximo
  * Implementação futura de SCD Tipo 2

---

#  Auditoria

Tabela: `etl_audit_log`

Campos principais:

| Campo          | Descrição                    |
| -------------- | ---------------------------- |
| process_name   | Nome do processo executado   |
| start_time     | Início da execução           |
| end_time       | Fim da execução              |
| status         | Sucesso / Falha              |
| rows_processed | Quantidade processada        |
| error_message  | Mensagem de erro (se houver) |

Objetivo:

* Monitoramento
* Rastreabilidade
* Governança

---

#  Estrutura do Projeto

```
data-pipeline/
│
├── airflow/
│   ├── dags/
│   └── logs/              # Ignorado no Git
│
├── src/
│   ├── ingestion/
│   ├── transform/
│   ├── warehouse/
│   └── data/
│       └── raw/           # Ignorado no Git
│
├── sql/
├── requirements.txt
└── .gitignore
```

---

#  Stack Tecnológica

| Tecnologia     | Finalidade               |
| -------------- | ------------------------ |
| Python         | Ingestão e transformação |
| PostgreSQL     | Data Warehouse           |
| Apache Airflow | Orquestração             |
| SQL            | Modelagem e consultas    |
| Git            | Versionamento            |

---




