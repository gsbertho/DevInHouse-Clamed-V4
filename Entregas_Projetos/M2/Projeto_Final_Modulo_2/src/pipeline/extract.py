from src.utils.gcs_utils import upload_file, read_csv_from_gcs

def upload_files_to_gcs() -> None:
    """
    Realiza o upload dos arquivos CSV locais para o Google Cloud Storage
    na camada Bronze (dados brutos).

    Fluxo:
        data/raw → GCS Bronze

    Arquivos:
        Origem:
            - data/raw/dim_filial.csv
            - data/raw/dim_produto.csv
            - data/raw/fato_vendas.csv

        Destino:
            - bronze/dim_filial.csv
            - bronze/dim_produto.csv
            - bronze/fato_vendas.csv

    Returns:
        None
    """

    #definir arquivos
    files = [
        "dim_filial.csv",
        "dim_produto.csv",
        "fato_vendas.csv"
    ]

    #loop para definir os paths, e executar cada upload
    for file in files:
        local_path = f"data/raw/{file}"
        gcs_path = f"bronze/{file}"

        upload_file(local_path, gcs_path)

    print("Extract concluído")

def extract_files_from_gcs() -> dict:
    """
    Realiza a leitura dos arquivos CSV armazenados na camada Bronze (GCS)
    e os carrega em DataFrames pandas.

    Fluxo:
        GCS Bronze → DataFrames (pandas)

    Arquivos lidos:
        - bronze/dim_filial.csv
        - bronze/dim_produto.csv
        - bronze/fato_vendas.csv

    Returns:
        dict:
            Dicionário contendo os DataFrames carregados:
                {
                    "filial": DataFrame com dados de filiais,
                    "produto": DataFrame com dados de produtos,
                    "vendas": DataFrame com dados de vendas
                }

    """

    df_filial = read_csv_from_gcs("bronze/dim_filial.csv")
    df_produto = read_csv_from_gcs("bronze/dim_produto.csv")
    df_vendas = read_csv_from_gcs("bronze/fato_vendas.csv")

    return {
        "filial": df_filial,
        "produto": df_produto,
        "vendas": df_vendas
    }