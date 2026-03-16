'''Pipeline para ingestão de dados por SCD2

def extract():
    pass

def transform():
    pass

def load():
    pass

def run_pipeline():
    extract()
    transform()
    load()

if __name__ == "__main__":
    run_pipeline()

CSV local
   │
   ▼
EXTRACT
   │
   ▼
GCS / bronze
   │
   ▼
TRANSFORM
(pandas)
   │
   ▼
GCS / silver
   │
   ▼
LOAD
(SQL MERGE)
   │
   ▼
BigQuery / gold

'''

from src.pipeline.extract import extract
from src.pipeline.transform import transform


def main():

    print("Iniciando pipeline")

    extract()

    transform()

    print("Pipeline finalizado")


if __name__ == "__main__":
    main()