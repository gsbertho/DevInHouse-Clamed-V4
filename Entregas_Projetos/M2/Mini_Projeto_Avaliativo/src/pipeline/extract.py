from src.utils.gcs_utils import upload_file

def extract():

    local_path = "data/iqvia_produtos.csv"
    gcs_path = "bronze/iqvia_produtos.csv"

    upload_file(local_path, gcs_path)

    print("Extract concluído")