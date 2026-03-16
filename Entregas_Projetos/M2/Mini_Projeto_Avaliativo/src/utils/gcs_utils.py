import os
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GCP_PROJECT_ID")
bucket_name = os.getenv("BUCKET_NAME")

credentials = service_account.Credentials.from_service_account_file(
    credentials_path
)

client = storage.Client(
    project=project_id,
    credentials=credentials
)

print("PROJECT:", os.getenv("GCP_PROJECT_ID"))
print("BUCKET:", os.getenv("BUCKET_NAME"))
print("CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def upload_file(local_file, destination_blob):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    blob.upload_from_filename(local_file)

    print(f"Upload concluído: {destination_blob}")

def download_file(blob_name, local_path):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.download_to_filename(local_path)

    print(f"Download concluído: {blob_name}")