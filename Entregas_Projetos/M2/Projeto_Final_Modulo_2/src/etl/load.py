from src.utils.postgres_utils import criar_conexao, executar_query
from psycopg2.extras import execute_values
from src.utils.logging_config import setup_logger

# Inicializa logger com o nome do módulo
logger = setup_logger(__name__)


def load_silver(dfs: dict):

    logger.info("Iniciando carga da camada Silver")

    conn = criar_conexao()
    cur = conn.cursor()

    # =========================
    # 1. CRIAR TABELAS (DDL)
    # =========================
    
    logger.info("Executando DDL para criação das tabelas Silver")

    with open("sql/silver/create_tables.sql", "r") as f:
        ddl_sql = f.read()

    for comando in ddl_sql.split(";"):
        comando = comando.strip()
        if comando:
            executar_query(comando, conn=conn)

    # =========================
    # 2. TRUNCATE
    # =========================

    logger.info("Executando TRUNCATE nas tabelas Silver")

    executar_query(
        "TRUNCATE silver.fato_vendas, silver.dim_produto, silver.dim_filial CASCADE",
        conn=conn
    )

    # =========================
    # 3. INSERT DIM_FILIAL
    # =========================

    logger.info("Inserindo dados na tabela dim_filial")

    execute_values(
        cur,
        """
        INSERT INTO silver.dim_filial (filial_id, brick, regiao, cluster)
        VALUES %s
        """,
        dfs["filial"].values.tolist()
    )

    # =========================
    # 4. INSERT DIM_PRODUTO
    # =========================

    logger.info("Inserindo dados na tabela dim_produto")

    execute_values(
        cur,
        """
        INSERT INTO silver.dim_produto (produto_id, categoria, nome_produto)
        VALUES %s
        """,
        dfs["produto"].values.tolist()
    )

    # =========================
    # 5. INSERT FATO
    # =========================

    logger.info("Inserindo dados na tabela fato_vendas")

    execute_values(
        cur,
        """
        INSERT INTO silver.fato_vendas (
            data, produto_id, filial_id, empresa,
            volume, preco_unitario, receita
        )
        VALUES %s
        """,
        dfs["vendas"].values.tolist()
    )

    conn.commit()
    cur.close()
    conn.close()

    logger.info("Carga Silver concluída")