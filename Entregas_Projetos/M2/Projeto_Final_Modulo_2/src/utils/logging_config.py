import logging
import os


def setup_logger(name: str = "pipeline_logger") -> logging.Logger:
    """
    Configura e retorna um logger padronizado para o projeto.

    Args:
        name (str): nome do logger (geralmente __name__ do módulo)

    Returns:
        logging.Logger: objeto logger configurado
    """

    logger = logging.getLogger(name)

    # Evita adicionar múltiplos handlers se já existir
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # =========================
    # FORMATO DO LOG
    # =========================
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    # =========================
    # HANDLER: CONSOLE
    # =========================
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # =========================
    # HANDLER: ARQUIVO
    # =========================
    os.makedirs("logs", exist_ok=True)

    file_handler = logging.FileHandler("logs/pipeline.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # =========================
    # ADICIONAR HANDLERS
    # =========================
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger