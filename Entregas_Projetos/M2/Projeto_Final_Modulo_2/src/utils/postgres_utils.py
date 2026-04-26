#imports
import psycopg2 as pg
from dotenv import load_dotenv
import os
from src.utils.logging_config import setup_logger

# Inicializa logger com o nome do módulo
logger = setup_logger(__name__)

# Lê o arquivo .env e carrega as informações para estabelecer a conexão postgresql
load_dotenv()  

#criar função para gerar conexão
def criar_conexao():
    """
    Cria e retorna uma conexão com o banco PostgreSQL
    utilizando as variáveis de ambiente definidas no arquivo .env.
    """
    try:
        conn = pg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT"),
            host=os.getenv("DB_HOST")
        )

        logger.info("Conexão realizada com sucesso")

        return conn
    
    except Exception as e:
        logger.error(f"Erro de conexão: {e}")
        raise


def executar_query(sql, params=None, conn=None):
    """
    Executa uma query SQL usando uma conexão existente (se passada)
    ou criando uma nova caso contrário.
    """
    auto_close = False

    try:
        #se nenhuma conexão for passada, cria e marca pra fechar no fim
        if conn is None:
            conn = criar_conexao()
            auto_close = True

        with conn.cursor() as cur:
            cur.execute(sql,params)

            #retornar resultados se for um select
            if sql.strip().lower().startswith("select"):
                return cur.fetchall()
            
             # demais comandos: gravar no banco
            conn.commit() 
            
        # para comandos que não retornam dados
        #print("Comando SQL executado com sucesso")
    
    except Exception as e:
        logger.error("Erro ao executar query:")
        logger.error(f"  ➤ SQL: {sql.strip()}")
        logger.error(f"  ➤ Parâmetros: {params}")
        logger.error(f"  ➤ Detalhes: {e}")
        conn.rollback()


    finally:
        # fecha a conexão apenas se foi criada aqui dentro
        if auto_close and conn:
            conn.close()