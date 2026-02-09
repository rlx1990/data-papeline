# Data Pipeline de Vendas

## Objetivo
Construir um pipeline de dados de vendas, desde a ingestão de dados brutos a partir de uma API pública até uma estrutura pronta para consumo em ferramentas de BI, seguindo boas práticas de engenharia de dados.

## Arquitetura
FakeStore API  
→ Ingestão (Python)  
→ Data Lake (raw → trusted → curated)  
→ Data Warehouse  
→ Power BI

## Stack
- Python
- Pandas / PyArrow
- PostgreSQL
- SQL

## Estrutura de Pastas
data/
- raw/ → dados brutos, sem qualquer transformação
- trusted/ → dados limpos e padronizados
- curated/ → dados modelados para analytics e BI

src/
- ingestion/ → scripts de ingestão de dados
- transformation/ → transformações e modelagem
- utils/ → funções auxiliares

## Status
Projeto em desenvolvimento.
