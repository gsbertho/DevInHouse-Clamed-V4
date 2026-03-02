import sqlite3
import os
import pandas as pd

#paths
PATH_DB = os.path.join(os.getcwd(),'db_gsb.db')

#funcoes
def conectar_db() -> sqlite3.Connection:
    """conecta o db_gsb.db do sqlite3"""

    return sqlite3.connect(PATH_DB)

with conectar_db() as conexao:
    df = pd.read_sql('select * from dim_produtos', con=conexao)
    print(df)