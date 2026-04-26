from src.etl.extract import upload_files_to_gcs
from src.utils.logging_config import setup_logger

# Inicializa logger com o nome do módulo
logger = setup_logger(__name__)

def run_bronze():
    logger.info("Iniciando pipeline Bronze")

    upload_files_to_gcs()
    logger.info("Upload para o GCS concluído")

    logger.info("Pipeline Bronze finalizado")