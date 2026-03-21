from src.utils.gcs_utils import upload_file

def extract() -> None:
    """
    Executa a etapa de extração do pipeline ETL.

    Realiza o upload de um arquivo CSV local para o bucket do Google Cloud Storage
    na camada Bronze (dados brutos).

    Fluxo:
        CSV local → GCS Bronze

    Arquivos:
        Origem: data/iqvia_produtos.csv
        Destino: bronze/iqvia_produtos.csv

    Returns:
        None
    """

    local_path = "data/iqvia_produtos.csv"
    gcs_path = "bronze/iqvia_produtos.csv"

    upload_file(local_path, gcs_path)

    print("Extract concluído")