from src.utils.gcs_utils import upload_file, read_csv_from_gcs
from src.utils.logging_config import setup_logger

# Inicializa logger com o nome do módulo
logger = setup_logger(__name__)

def upload_files_to_gcs() -> None:
    """
    Realiza o upload dos arquivos CSV locais para o Google Cloud Storage
    na camada Bronze (dados brutos).
    """

    logger.info("Iniciando upload de arquivos para o GCS (Bronze)")

    files = [
        "dim_filial.csv",
        "dim_produto.csv",
        "fato_vendas.csv"
    ]

    for file in files:
        local_path = f"data/raw/{file}"
        gcs_path = f"bronze/{file}"

        logger.info(f"Enviando arquivo: {file}")
        upload_file(local_path, gcs_path)

    logger.info("Upload de arquivos concluído (Bronze)")


def extract_files_from_gcs() -> dict:
    """
    Realiza a leitura dos arquivos CSV armazenados na camada Bronze (GCS)
    e os carrega em DataFrames pandas.
    """

    logger.info("Iniciando leitura dos arquivos do GCS (Bronze)")

    df_filial = read_csv_from_gcs("bronze/dim_filial.csv")
    logger.info("Arquivo dim_filial.csv carregado")

    df_produto = read_csv_from_gcs("bronze/dim_produto.csv")
    logger.info("Arquivo dim_produto.csv carregado")

    df_vendas = read_csv_from_gcs("bronze/fato_vendas.csv")
    logger.info("Arquivo fato_vendas.csv carregado")

    logger.info("Leitura dos arquivos do GCS concluída")

    return {
        "filial": df_filial,
        "produto": df_produto,
        "vendas": df_vendas
    }