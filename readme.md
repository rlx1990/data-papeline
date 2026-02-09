# Fakestore Data Pipeline

Projeto de engenharia de dados com foco em ingestão, transformação e modelagem de dados a partir de uma API pública de e-commerce.

## Objetivo
Construir um pipeline de dados completo utilizando a Fakestore API, organizando os dados nas camadas:
- Raw
- Trusted
- Curated

## Fonte de Dados
- Fakestore API  
  https://fakestoreapi.com/

Endpoints utilizados:
- `/products`
- `/users`
- `/carts`

## Stack
- Python
- Requests
- JSON
- Git / GitHub

## Arquitetura (visão geral)
API → Raw (JSON) → Trusted → Curated → BI

