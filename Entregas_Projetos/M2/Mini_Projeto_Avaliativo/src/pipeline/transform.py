from src.utils.gcs_utils import upload_file, read_csv_from_gcs
import pandas as pd


def tratar_dim_produto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para carga em uma dimensão com SCD Tipo 2.

    A função adapta o dataset original para conter apenas as colunas
    necessárias para o controle de histórico no BigQuery.

    Transformações:
        - Seleção e renomeação de colunas relevantes
        - Remoção de registros inválidos
        - Padronização de tipos
        - Remoção de duplicidades

    Args:
        df (pd.DataFrame): DataFrame bruto vindo da camada Bronze

    Returns:
        pd.DataFrame: DataFrame com colunas prontas para staging
    """

    df = df.rename(
        columns={
            'Cod Prod Catarinense': 'id_produto_original',
            'Tipo Informacao SO Bandeira PRECO POPULAR Unidade': 'valor_produto'
        }
    )

    # mantém apenas colunas necessárias
    df = df[['id_produto_original', 'valor_produto']]

    # remove registros inválidos
    df = df.dropna(subset=['id_produto_original'])

    # padronizar como INT o id_produto_original
    df["id_produto_original"] = df["id_produto_original"].astype(int)

    # trata valor
    df['valor_produto'] = (
        df['valor_produto']
        .fillna(0)
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # remove duplicados
    df = df.drop_duplicates()

    return df


def transform() -> pd.DataFrame:
    """
    Executa a etapa de transformação do pipeline ETL.

    Responsável por:
        - Ler dados da camada Bronze (GCS)
        - Aplicar transformação de negócio via `tratar_dim_produto`
        - Armazenar os dados tratados na camada Silver (Parquet no GCS)

    Fluxo:
        GCS Bronze → pandas → tratar_dim_produto → Parquet → GCS Silver

    Arquivos:
        Origem (GCS): bronze/iqvia_produtos.csv
        Destino (GCS): silver/iqvia_produtos.parquet

    Returns:
        None
    """

    bronze_blob = "bronze/iqvia_produtos.csv"

    silver_local = "data/silver_dim_produto.parquet"
    silver_blob = "silver/silver_dim_produto.parquet"

    #LEITURA
    #ler csv da camada bronze do gcs e armazenar como DataFrame
    df = read_csv_from_gcs(bronze_blob,sep=";",decimal=",")

    #TRANSFORMAÇÃO
    #ler DataFrame, tratar e retornar um DataFrame
    df = tratar_dim_produto(df)

    #ARMAZENAMENTO LOCAL
    #salvar o DataFrame tratado em um arquivo parquet na camada silver local
    df.to_parquet(silver_local, index=False)

    #UPLOAD PARA GCS
    #salvar o arquivo parquet da camada silver local na camada silver do gcs
    upload_file(silver_local, silver_blob)

    print("Transform concluído")

    return df