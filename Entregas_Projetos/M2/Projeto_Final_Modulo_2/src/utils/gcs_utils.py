import os
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GCP_PROJECT_ID")
bucket_name = os.getenv("BUCKET_NAME")

credentials = service_account.Credentials.from_service_account_file(
    credentials_path
)

client = storage.Client(
    project=project_id,
    credentials=credentials
)

#remover depois ou usar logging
# print("PROJECT:", os.getenv("GCP_PROJECT_ID"))
# print("BUCKET:", os.getenv("BUCKET_NAME"))
# print("CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def upload_file(local_path: str, gcs_path: str) -> None:
    """
    Faz upload de um arquivo local para o Google Cloud Storage.

    Args:
        local_path (str): Caminho do arquivo no ambiente local.
        gcs_path (str): Caminho de destino no bucket (ex: bronze/arquivo.csv).

    Returns:
        None
    """
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    blob.upload_from_filename(local_path)

    print(f"Upload concluído: {gcs_path}")


def read_csv_from_gcs(gcs_path: str, sep: str = ",", decimal: str = ".") -> pd.DataFrame:
    """
    Lê um CSV diretamente do GCS e retorna um DataFrame pandas.
    """
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    with blob.open("r") as f:
        df = pd.read_csv(f, sep=sep, decimal=decimal)

    return df