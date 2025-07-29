from botocore.exceptions import ClientError
from botocore.config import Config
from dotenv import load_dotenv
from datetime import datetime
import boto3
import os

load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("S3_REGION_NAME")

s3_config = Config(
    signature_version='v4'
)

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name = REGION_NAME,
    config=s3_config,
)

def generate_presigned_url(filename: str, content_type: str):

    timestamp = datetime.utcnow().time()
    key_url = f"{timestamp}_{filename}"
    
    try: 
        presigned = s3.generate_presigned_url(
        "put_object",
        Params = {'Bucket': BUCKET_NAME, "Key": key_url, "ContentType": content_type},
        ExpiresIn=300
    )
    except ClientError as e:
        print(e)
        return
    
    return presigned
