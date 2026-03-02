"""
conectar/criar um db local
criar duas tabelas vazias via SQL no python

dim_produtos:
id_produto,
nome,
preco.

dim_clientes:
id_cliente,
nome,
endereco,
is_current (booleano)
dt_inicio (texto/data)
"""

#imports
import sqlite3
import os
import pandas as pd

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


def executar_etl() -> None:
    with conectar_db() as conexao:
        criar_dimensoes(conexao)


if __name__ == "__main__":
    executar_etl()