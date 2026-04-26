from src.utils.postgres_utils import criar_conexao, executar_query
from src.utils.logging_config import setup_logger

# Inicializa logger com o nome do módulo
logger = setup_logger(__name__)

def run_gold():
    logger.info("Iniciando pipeline Gold")

    conn = criar_conexao()

    with open("sql/gold/views.sql", "r") as f:
        sql = f.read()

    for comando in sql.split(";"):
        comando = comando.strip()
        if comando:
            executar_query(comando, conn=conn)

    conn.close()

    logger.info("Camada Gold criada com sucesso")