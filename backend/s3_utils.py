import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY
)

file_name = 's3test.txt'
key = "test-folder/s3test.txt"

s3.upload_file(file_name, BUCKET_NAME, key)
print(f"Uploaded {file_name} to s3://{BUCKET_NAME}/{key}")

s3.download_file(BUCKET_NAME, key, "downloaded.txt")
print("Downloaded back to downloaded.txt")