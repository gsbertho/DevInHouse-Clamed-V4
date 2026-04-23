import pandas as pd

def transform_to_silver(dfs: dict) -> dict:
    """
    Realiza a transformação inicial dos dados (camada Silver):
    - Conversão de tipos
    - Tratamento de inconsistências
    - Padronização básica

    Regra de negócio:
        Conforme exploração prévia das tabelas, notou-se padronização correta nas tabelas dimensão
        produto e dimensão filial, na tabela fato vendas percebeu-se a existência de situações
        de volume nulo e/ou receita inválida (receita unitária permaneceu coerente), de tal
        forma que foi decidido:
        - casos com volume nulo mas com receita preenchida, calcula-se volume
        - casos com volume nulo mas com receita nula, considera-se que não houve venda, zerando tanto
        o volume quanto a receita.
        

    Args:
        dfs (dict): dicionário com DataFrames do extract

    Returns:
        dict: DataFrames tratados
    """

    df_filial = dfs["filial"].copy()
    df_produto = dfs["produto"].copy()
    df_vendas = dfs["vendas"].copy()

    # =========================
    # TRATAMENTO FATO_VENDAS
    # =========================

    # padronização de tipo - converter data
    df_vendas["data"] = pd.to_datetime(df_vendas["data"], errors="coerce")

    # tratar receitas inválidas
    df_vendas["receita"] = df_vendas["receita"].replace("#VALUE!", None)
    df_vendas["receita"] = pd.to_numeric(df_vendas["receita"], errors="coerce")


    ###### tratamento de volume ######

    # criar mascara de casos tratáveis
    mask_recuperavel = (
        df_vendas["volume"].isna()
        & df_vendas["receita"].notna()
        & df_vendas["preco_unitario"].notna()
    )

    # calcular volume como número inteiro nos casos aplicáveis
    df_vendas.loc[mask_recuperavel, "volume"] = (
        df_vendas.loc[mask_recuperavel, "receita"]
        / df_vendas.loc[mask_recuperavel, "preco_unitario"]
    ).round(0)

    # criar mascara de casos irrecuperáveis, considerando tratamento prévio já realizado
    mask_irrecuperavel = df_vendas["volume"].isna()

    # padronizar valores de acordo com a regra de negócio definida
    df_vendas.loc[mask_irrecuperavel, "volume"] = 0
    df_vendas.loc[mask_irrecuperavel, "receita"] = 0

    # padronização de tipo - converter volume para inteiro
    df_vendas["volume"] = df_vendas["volume"].astype("Int64")
 

    # =========================
    # TRATAMENTO GERAL
    # =========================

    # remoção de duplicatas
    df_filial = df_filial.drop_duplicates()
    df_produto = df_produto.drop_duplicates()
    df_vendas = df_vendas.drop_duplicates()

    # exibir duplicatas removidas
    print("Duplicados removidos (filial):", len(dfs["filial"]) - len(df_filial))
    print("Duplicados removidos (produto):", len(dfs["produto"]) - len(df_produto))
    print("Duplicados removidos (vendas):", len(dfs["vendas"]) - len(df_vendas))

    return {
        "filial": df_filial,
        "produto": df_produto,
        "vendas": df_vendas
    }