"""
Pipeline para ingestão de dados com SCD2
"""

from src.pipeline.extract import extract
from src.pipeline.transform import transform
from src.pipeline.load import load, simular_alteracoes

from src.utils.bq_utils import (
    criar_tabela_dim_produto,
    criar_tabela_stg_produto
)

def main(simular: bool = False):

    print("\n=== INICIANDO PIPELINE ===")

    # 1. extract
    extract()

    # 2. transform
    df = transform()

    # 3. simulação opcional
    if simular:
        print("\n=== APLICANDO SIMULAÇÃO ===")
        df = simular_alteracoes(df)

    # 4. load
    load(df)

    print("\n=== PIPELINE FINALIZADO ===")


if __name__ == "__main__":
    main(simular=False)