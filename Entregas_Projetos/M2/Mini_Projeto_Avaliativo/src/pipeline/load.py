import pandas as pd
from src.utils.bq_utils import (
    executar_query,
    upload_dataframe,
    criar_tabela_dim_produto,
    criar_tabela_stg_produto,
    DATASET,
    PROJECT_ID
)

def fechar_registros_alterados() -> None:
    """
    Fecha registros ativos que sofreram alteração.
    """

    tabela_dim = f"{PROJECT_ID}.{DATASET}.dim_produto"
    tabela_stg = f"{PROJECT_ID}.{DATASET}.stg_produto"

    sql = f"""
    UPDATE `{tabela_dim}` T
    SET
        data_fim_validade = CURRENT_DATE(),
        flag_ativo = FALSE
    FROM `{tabela_stg}` S
    WHERE
        T.id_produto_original = S.id_produto_original
        AND T.flag_ativo = TRUE
        AND T.valor_produto != S.valor_produto
    """

    executar_query(sql)

def inserir_novos_registros() -> None:
    """
    Insere novos produtos e novas versões usando MERGE.
    """

    tabela_dim = f"{PROJECT_ID}.{DATASET}.dim_produto"
    tabela_stg = f"{PROJECT_ID}.{DATASET}.stg_produto"

    sql = f"""
    MERGE `{tabela_dim}` AS dim
    USING (
        SELECT 
            S.id_produto_original,
            S.valor_produto
        FROM `{tabela_stg}` S
        LEFT JOIN `{tabela_dim}` T
            ON T.id_produto_original = S.id_produto_original
            AND T.flag_ativo = TRUE
        WHERE
            T.id_produto_original IS NULL
            OR T.valor_produto != S.valor_produto
    ) AS novos
    ON FALSE

    WHEN NOT MATCHED THEN
        INSERT (
            sk_produto,
            id_produto_original,
            valor_produto,
            data_inicio_validade,
            data_fim_validade,
            flag_ativo
        )
        VALUES (
            GENERATE_UUID(),
            novos.id_produto_original,
            novos.valor_produto,
            CURRENT_DATE(),
            NULL,
            TRUE
        )
    """

    executar_query(sql)

def simular_alteracoes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simula:
    - alteração de valor de um produto existente
    - inclusão de um novo produto
    """

    df_simulado = df.copy()

    # 1. alterar um produto existente
    # altera o primeiro produto do df
    if not df_simulado.empty:
        idx = df_simulado.index[0]
        df_simulado.loc[idx, "valor_produto"] += 10

    # 2. inserir novo produto
    novo_produto = pd.DataFrame({
        "id_produto_original": [999999],
        "valor_produto": [999.99]
    })

    df_simulado = pd.concat([df_simulado, novo_produto], ignore_index=True)

    return df_simulado

def load(df) -> None:
    """
    Executa o processo de carga no BigQuery.

    Fluxo:
        1. Garante existência das tabelas
        2. Carrega staging
        3. Executa SCD2 (UPDATE + INSERT)
    """

    tabela_stg = f"{PROJECT_ID}.{DATASET}.stg_produto"

    # 1. garantir estrutura (idempotente)
    criar_tabela_stg_produto()
    criar_tabela_dim_produto()

    # 2. staging
    upload_dataframe(df, tabela_stg)

    # 3. SCD2
    fechar_registros_alterados()
    inserir_novos_registros()

    print("Load concluído")