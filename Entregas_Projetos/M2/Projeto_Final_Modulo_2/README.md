# projeto-etl-vendas-market-share

Repositório para entrega do projeto final do módulo 2 do curso DevInHouse Clamed - V4 - Analista de Dados.

---

## Informações gerais

Projeto de dados desenvolvido em Python utilizando arquitetura em camadas (Bronze / Silver / Gold), com integração ao Google Cloud Storage (GCS), PostgreSQL e visualização de dados via Streamlit.

O projeto contempla todo o fluxo de dados, desde a ingestão de arquivos CSV, passando por etapas de transformação e modelagem com pandas e SQL, até a disponibilização de informações estruturadas para análise.

Além do pipeline ETL, o foco principal está na análise dos dados, com a construção de indicadores de negócio a partir das informações processadas. Esses insights são explorados por meio de um dashboard interativo, permitindo a interpretação dos resultados e apoiando a tomada de decisão.

---

## Arquitetura do Pipeline

### O pipeline segue o padrão:

```markdown
CSV Local (data/raw)
│
▼
EXTRACT (upload para GCS)
│
▼
GCS - Bronze (dados brutos, imutáveis)
│
▼
EXTRACT (leitura do GCS)
│
▼
TRANSFORM (pandas - limpeza, tipagem, deduplicação)
│
▼
LOAD (PostgreSQL)
│
▼
PostgreSQL - Silver (tabelas estruturadas)
│
▼
TRANSFORM (SQL - views e agregações)
│
▼
PostgreSQL - Gold (views analíticas)
│
▼
Streamlit (dashboard)
```

---

### Camadas

* **Bronze** → dados brutos armazenados no GCS (simulando um datalake)
* **Silver** → dados tratados e estruturados no PostgreSQL
* **Gold** → views analíticas para consumo
* **App** → visualização e análise via Streamlit

---

### Observação sobre a ingestão de dados na camada Bronze:

Neste projeto, a ingestão dos dados iniciais é simulada e realizada pelo próprio pipeline, que envia os arquivos CSV (dados brutos) para o Google Cloud Storage, representando uma fonte externa. Em um cenário real, essa etapa consistiria apenas na extração de dados já disponibilizados por outros sistemas. Assim, a abordagem adotada permite simular de ponta a ponta o fluxo de ingestão e leitura de dados a partir de um datalake.

---

### Comportamento do pipeline

O foco deste projeto não é apenas o ETL, portanto não utiliza das técnicas de SCD.
Para ainda assim garantir a idempotência do projeto:

* As tabelas da camada Silver são truncadas e recarregadas  a cada execução do pipeline
* A camada Gold é composta por views analíticas também recriadas a cada execução

---

**Importante**

* O pipeline depende de credenciais válidas do GCS 
* O pipeline depende de um servidor Postgres instalado

---

## Tecnologias utilizadas

- Python  
- Pandas (tratamento e transformação de dados)  
- PostgreSQL (armazenamento e camada analítica)  
- Google Cloud Storage - GCS (armazenamento de dados brutos)  
- Streamlit (visualização e dashboards interativos)  
- Matplotlib e Seaborn (visualizações)  
- psycopg2 (integração com PostgreSQL via Python)  

---

## Estrutura do projeto

```markdown
projeto-etl-vendas-market-share/

├── main.py
├── requirements.txt
├── .env
├── README.md

├── data/
│   └── raw/

├── sql/
│   ├── silver/
│   │   └── create_tables.sql
│   └── gold/
│       └── views.sql

├── src/
│   ├── pipeline/
│   │   ├── bronze.py
│   │   ├── silver.py
│   │   └── gold.py
│   │
│   ├── etl/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   │
│   └── utils/
│       ├── gcs_utils.py
│       ├── postgres_utils.py
│       └── logging_config.py

├── credentials/
│   └── service_account.json

├── logs/

├── st_dashboard.py
```
**Observações:**

- O arquivo `.env` deve ser criado localmente com as variáveis de ambiente necessárias  
- A pasta `credentials/` deve conter as credenciais do GCP
- A pasta `logs/` armazena os logs gerados durante a execução do pipeline  


---

## Configuração

Criar um arquivo `.env` com as variáveis:

```markdown
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_HOST=localhost
DB_PORT=5432

GOOGLE_APPLICATION_CREDENTIALS=credentials/service_account.json
GCP_PROJECT_ID=seu_projeto
BUCKET_NAME=seu_bucket
```

---

## Instalação

Instalar as dependências do projeto:

```markdown
pip install -r requirements.txt
```

---

## Execução

### Executar pipeline completo:
**Observação:**

O arquivo main.py apresenta a opção de executar ou não a ingestão de dados no GCS, de forma que a etapa Silver começa por extrair o que já foi carregado no GCS anteriormente.

```markdown
python main.py
```

### Executar dashboard:
Após executar o pipeline, executar o dashboard:

```markdown
streamlit run st_dashboard.py
```

---

## Principais análises

O dashboard desenvolvido apresenta:

* Market Share por volume e receita
* Gap de preço médio (Clamed vs concorrência)
* Identificação de bricks com maior potencial de crescimento
* Evolução temporal de vendas
* Análise de volume por produto
* Distribuição de vendas por brick

---

## Validação SQL

Consulta exemplo no PostgreSQL:

```markdown
SELECT *
FROM gold.vw_market_share_mensal
ORDER BY mes, brick;
```

---


## Observações Finais

O projeto é uma simplificação de um processo completo de ETL e consumo de dados para análise, ainda assim tive o cuidado de garantir a consistência dos dados e seus significados. 

Foram colocadas algumas observações sobre decisões técnicas e de arquitetura nas funções e no código em geral. Simplificações as vezes necessárias, padronizações conforme limitações da base de dados, etc.


Um exemplo é na exploração dos dados, que procurei garantir a integridade das relações conforme relacionamento de colunas e tabelas, onde garanti que o filtro funcionasse para os 3 DataFrames criados, ainda que 2 deles viessem direto de views da camada Gold enquanto o terceiro vem de uma consulta DQL baseada na camada Silver.

Verificadas limitações nos dados brutos, optei por não explorar tanto os agrupamentos em relação à dimensão de filiais, pois um mesmo brick apresentava diferentes regiões, dificultando relacionamentos em agrupamentos. Sendo assim, segui apenas com os filtros obrigatórios e explorei tabelas agregadas por categoria de produtos e uma tabela aberta a nível de SKU.

---