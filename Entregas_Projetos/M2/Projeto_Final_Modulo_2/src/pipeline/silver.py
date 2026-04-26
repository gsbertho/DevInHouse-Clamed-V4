from src.etl.extract import extract_files_from_gcs
from src.etl.transform import transform_to_silver
from src.etl.load import load_silver
from src.utils.logging_config import setup_logger

# Inicializa logger com o nome do módulo
logger = setup_logger(__name__)

def run_silver():
    logger.info("Iniciando pipeline Silver")

    dfs = extract_files_from_gcs()
    logger.info("Dados extraídos do GCS")

    dfs = transform_to_silver(dfs)
    logger.info("Transformação concluída")

    load_silver(dfs)
    logger.info("Carga no PostgreSQL concluída")