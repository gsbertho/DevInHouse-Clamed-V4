from src.utils.gcs_utils import upload_file, download_file
import pandas as pd


def transform():

    bronze_blob = "bronze/iqvia_produtos.csv"
    bronze_local = "data/bronze_temp.csv"

    silver_local = "data/silver_produtos.parquet"
    silver_blob = "silver/iqvia_produtos.parquet"

    download_file(bronze_blob, bronze_local)

    df = pd.read_csv(bronze_local, sep=";")

    df = df.drop_duplicates()

    df.to_parquet(silver_local, index=False)

    upload_file(silver_local, silver_blob)

    print("Transform concluído")