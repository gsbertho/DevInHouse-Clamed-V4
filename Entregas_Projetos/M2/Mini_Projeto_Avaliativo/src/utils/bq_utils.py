from google.cloud import bigquery
from dotenv import load_dotenv
import os

# carrega variáveis do .env
load_dotenv()

DATASET = os.getenv("DATASET_NAME")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")

# cria cliente
client = bigquery.Client(project=PROJECT_ID)


def executar_query(sql: str) -> None:
    """
    Executa uma query no BigQuery.

    Args:
        sql (str): Query SQL a ser executada

    Returns:
        None
    """

    job = client.query(sql)
    job.result()

    print("Query executada com sucesso")

def criar_tabela_dim_produto() -> None:
    """
    Cria a tabela dim_produto no BigQuery (caso não exista).
    """

    tabela = f"{PROJECT_ID}.{DATASET}.dim_produto"

    sql = f"""
    CREATE TABLE IF NOT EXISTS `{tabela}` (
        sk_produto STRING,
        id_produto_original INT64,
        valor_produto FLOAT64,
        data_inicio_validade DATE,
        data_fim_validade DATE,
        flag_ativo BOOL
    )
    """

    executar_query(sql)

def criar_tabela_stg_produto() -> None:
    """
    Cria a tabela stg_produto no BigQuery (caso não exista).
    """

    tabela = f"{PROJECT_ID}.{DATASET}.stg_produto"

    sql = f"""
    CREATE TABLE IF NOT EXISTS `{tabela}` (
        id_produto_original INT64,
        valor_produto FLOAT64
    )
    """

    executar_query(sql)

def upload_dataframe(df, tabela: str) -> None:
    """
    Envia um DataFrame pandas para uma tabela no BigQuery,
    sobrescrevendo os dados existentes (staging).

    Args:
        df (pd.DataFrame): DataFrame a ser enviado
        tabela (str): Nome completo da tabela (project.dataset.tabela)

    Returns:
        None
    """

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"  # sobrescreve staging
    )

    job = client.load_table_from_dataframe(
        df,
        tabela,
        job_config=job_config
    )

    job.result()

    print(f"Dados carregados para {tabela}")