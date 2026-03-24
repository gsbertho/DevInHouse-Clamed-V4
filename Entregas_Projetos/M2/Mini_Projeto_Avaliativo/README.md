# projeto-etl-iqvia-scd2
Repositório para entrega do mini-projeto do módulo 2 do curso DevInHouse Clamed - V4 - Analista de Dados.

---

## Informações gerais

Projeto de pipeline ETL desenvolvido em Python utilizando arquitetura em camadas (Bronze / Silver / Gold), integração com Google Cloud Platform e Google BigQuery.

O objetivo do projeto é realizar a ingestão de dados a partir de um arquivo CSV, aplicar transformações com pandas e carregar os dados no BigQuery utilizando a estratégia SCD Tipo 2 para controle de histórico.

---

## Arquitetura do Pipeline

O pipeline segue o padrão:

````markdown
CSV Local
│
▼
EXTRACT (upload para GCS)
│
▼
GCS - Bronze (dados brutos)
│
▼
TRANSFORM (pandas)
│
▼
GCS - Silver (parquet tratado)
│
▼
LOAD (BigQuery - SCD Tipo 2)
│
▼
BigQuery - Gold (dim_produto)
````


### Camadas:

- **Bronze** → dados brutos no GCS
- **Silver** → dados tratados e padronizados  
- **Gold** → dados modelados no BigQuery com histórico  

---

## Tecnologias utilizadas

- Python
- Pandas
- Google Cloud Storage (GCS)
- BigQuery
- PyArrow
- python-dotenv

---

## Regras de negócio

O projeto implementa **SCD Tipo 2**, garantindo:

- Inserção de novos registros
- Versionamento de alterações
- Controle de histórico com:
  - `data_inicio_validade`
  - `data_fim_validade`
  - `flag_ativo`

---

## Estrutura do projeto

````markdown
Mini_Projeto_Avaliativo/

│
├── main.py
├── requirements.txt
├── .env
├── README.md
│
├── data/
│ └── iqvia_produtos.csv
│
├── credentials/
│ └── service_account.json
│
├── src/
│ ├── pipeline/
│ │ ├── extract.py
│ │ ├── transform.py
│ │ └── load.py
│ │
│ └── utils/
│ ├── gcs_utils.py
│ └── bq_utils.py
````
---

## Configuração

Criar um arquivo `.env` com as variáveis:

GOOGLE_APPLICATION_CREDENTIALS=credentials/service_account.json  
GCP_PROJECT_ID=seu_projeto  
BUCKET_NAME=seu_bucket  
DATASET_NAME=seu_dataset  

---

## Instalação

Instalar as dependências do projeto:

pip install -r requirements.txt

---

## Execução

Executar o pipeline:

python main.py
(selecionar simular=False ou simular=True para gerar simulação de alteração de dados e inclusão de dados)

---

## Comportamento do pipeline

O pipeline foi construído para ser idempotente.

- Primeira execução: realiza a carga inicial dos dados  
- Segunda execução: não gera alterações (dados permanecem consistentes)  
- Execução com simulação: aplica alterações e insere novos registros, gerando histórico via SCD Tipo 2  

---

## Validação

Consulta básica para verificação no BigQuery:

SELECT *
FROM dim_produto
ORDER BY id_produto_original, data_inicio_validade;

---

## Observações

- As tabelas são criadas automaticamente durante a execução do load  
- A camada Gold é mantida no BigQuery por se tratar de dados analíticos  
- O pipeline pode ser executado múltiplas vezes sem gerar inconsistências  

---