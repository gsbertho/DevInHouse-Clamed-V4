from src.pipeline.bronze import run_bronze
from src.pipeline.silver import run_silver
from src.pipeline.gold import run_gold
from src.utils.logging_config import setup_logger

logger = setup_logger(__name__)


def main(run_bronze_flag: bool = False):
    """
    Orquestra o pipeline completo.

    Args:
        run_bronze_flag (bool): se True, executa o upload para o GCS.
                               (simular a ingestão dos arquivos locais na camada bronze)
    """

    if run_bronze_flag:
        logger.info("=== Rodando Bronze ===")
        run_bronze()

    logger.info("=== Rodando Silver ===")
    run_silver()

    logger.info("=== Rodando Gold ===")
    run_gold()

    logger.info("=== Pipeline finalizado com sucesso ===")


if __name__ == "__main__":
    main(run_bronze_flag=False)