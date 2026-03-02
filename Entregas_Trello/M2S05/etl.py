#imports
import sqlite3
import os
import pandas as pd
from datetime import datetime

#paths
PATH_DADOS = os.path.join(os.getcwd(),'dados')
PATH_PRODUTOS = os.path.join(PATH_DADOS,'produtos.csv')
PATH_CLIENTES = os.path.join(PATH_DADOS,'clientes.csv')
PATH_DB = os.path.join(os.getcwd(),'db_gsb.db')

#funcoes
def conectar_db() -> sqlite3.Connection:
    """conecta o db_gsb.db do sqlite3"""

    return sqlite3.connect(PATH_DB)

def criar_dimensoes(conexao: sqlite3.Connection) -> None:
    #criar as tabelas no banco de dados local sqlite3

    cursor = conexao.cursor()

    #criar tabela produtos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dim_produtos (
            id_produto INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
        """
    )

    #criar tabela clientes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dim_clientes (
            id_cliente INTEGER NOT NULL,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            is_current INTEGER NOT NULL,
            dt_inicio TEXT NOT NULL
        )
        """
    )

    #commitar criacoes para salvar
    conexao.commit()

def carregar_stg(conexao: sqlite3.Connection) -> None:
    """Ex 3 - ler dados csv e carregar em tabelas staging"""

    #conferencia existencia arquivos
    if not os.path.exists(PATH_PRODUTOS) or not os.path.exists(PATH_CLIENTES):
        raise FileNotFoundError('Arquivo CSV não encontrado, gerar os dados primeiro')
    
    df_produtos = pd.read_csv(PATH_PRODUTOS)
    df_clientes = pd.read_csv(PATH_CLIENTES)

    #criar tabelas stg no banco de dados sqlite3
    df_produtos.to_sql('stg_produtos', conexao, if_exists='replace', index=False)
    df_clientes.to_sql('stg_clientes', conexao, if_exists='replace',index=False)

def aplicar_scd_tipo_1_produtos(conexao: sqlite3.Connection) -> None:
    """ex4 - SCD Tipo 1: atualiza preço e insere novos produtos."""
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE dim_produtos
           SET nome = (SELECT stg.nome
                         FROM stg_produtos stg
                        WHERE stg.id_produto = dim_produtos.id_produto),
               preco = (SELECT stg.preco
                          FROM stg_produtos stg
                         WHERE stg.id_produto = dim_produtos.id_produto)
         WHERE id_produto IN (SELECT id_produto FROM stg_produtos)
           AND (
               preco <> (SELECT stg.preco
                           FROM stg_produtos stg
                          WHERE stg.id_produto = dim_produtos.id_produto)
            OR nome <> (SELECT stg.nome
                          FROM stg_produtos stg
                         WHERE stg.id_produto = dim_produtos.id_produto)
           )
        """
    )

    cursor.execute(
        """
        INSERT INTO dim_produtos (id_produto, nome, preco)
        SELECT stg.id_produto, stg.nome, stg.preco
          FROM stg_produtos stg
          LEFT JOIN dim_produtos dim
            ON dim.id_produto = stg.id_produto
         WHERE dim.id_produto IS NULL
        """
    )

    conexao.commit()


def aplicar_scd_tipo_2_clientes(conexao: sqlite3.Connection) -> None:
    """ex 4 - SCD Tipo 2: preserva histórico de endereço."""
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE dim_clientes
           SET is_current = 0
         WHERE is_current = 1
           AND EXISTS (
               SELECT 1
                 FROM stg_clientes stg
                WHERE stg.id_cliente = dim_clientes.id_cliente
                  AND stg.endereco <> dim_clientes.endereco
           )
        """
    )

    cursor.execute(
        """
        INSERT INTO dim_clientes (id_cliente, nome, endereco, is_current, dt_inicio)
        SELECT stg.id_cliente, stg.nome, stg.endereco, 1, ?
          FROM stg_clientes stg
          LEFT JOIN dim_clientes dim_atual
            ON dim_atual.id_cliente = stg.id_cliente
           AND dim_atual.is_current = 1
         WHERE dim_atual.id_cliente IS NULL
            OR dim_atual.endereco <> stg.endereco
        """,
        (agora,),
    )

    conexao.commit()


def executar_etl() -> None:
    with conectar_db() as conexao:
        criar_dimensoes(conexao)
        carregar_stg(conexao)
        aplicar_scd_tipo_1_produtos(conexao)
        aplicar_scd_tipo_2_clientes(conexao)


if __name__ == "__main__":
    executar_etl()