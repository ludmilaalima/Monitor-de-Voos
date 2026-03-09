# Monitor de Tarifas Aéreas — em desenvolvimento

Aplicação web voltada à engenharia de dados para coletar preços de passagens no Google Flights, construir histórico de preços por hora/dia e apoiar a decisão de compra com inteligência de preços (detecção de quedas, picos e janelas de oportunidade).

## Status
🚧 Em desenvolvimento — MVP em construção.

## Objetivo
- Registrar histórico de tarifas ao longo do tempo
- Permitir consultas e comparações de variação de preço
- Evoluir para análises e alertas de “melhor momento de compra”

## Funcionalidades (atual)
- Formulário web (HTML) para entrada de parâmetros (origem, destino, datas etc.)
- Coleta inicial automatizada com Selenium (Google Flights)
- API em Python (FastAPI) recebendo os parâmetros e disparando a coleta
- Persistência/armazenamento:  JSON/CSV e Banco de dados

## Roadmap (planejado)
- Orquestração e agendamentos com Apache Airflow (coletas horárias/diárias, retries, logs)
- Camadas Bronze/Silver/Gold + padronização de schema
- Armazenamento analítico em Parquet / Data Lake (particionado por data/hora)
- Transformações e testes com dbt
- Processamento distribuído com Apache Spark
- Deploy e/ou serviços em nuvem (AWS/Azure/GCP)
- Monitoramento e qualidade de dados (validações de consistência, deduplicação, alertas)

## Arquitetura
Usuário (Web) → FastAPI → Selenium (ingestão) → Storage (Bronze) → Transformações (Silver/Gold) → Consultas/Análises

## Stack
**Atual:** Python (FastAPI) | Selenium | HTML | JavaScript | SQL (básico)  
**Planejada:** CSS | Apache Airflow | Apache Spark | Parquet/Data Lake | dbt | Cloud (AWS/Azure/GCP)

## Como rodar localmente
> **EM CONSTRUÇÃO**
