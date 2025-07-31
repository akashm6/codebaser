from parallel_processing.multiprocessor import concurrent_parse
from s3_utils import generate_presigned_url, s3
from fastapi import APIRouter, Query
from dotenv import load_dotenv
from pydantic import BaseModel
import tempfile
import zipfile
import boto3
import os

load_dotenv()

class ZipFileModel(BaseModel):
    s3_key: str
    name: str
    content_type: str
    size: int

router = APIRouter()
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@router.get("/generate-presigned-url")
def get_presigned_url(filename: str = Query(...), content_type: str = Query(...)):
    return generate_presigned_url(filename, content_type)

@router.post("/zip-processing")
def process_zip(zip: ZipFileModel):

    s3_key = zip.s3_key
    # frontend has uploaded zip to s3, fetch the s3 file and download a temp file from it
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:

        temp_path = temp_file.name
        s3.download_file(BUCKET_NAME, s3_key, temp_path)
        # unzip and begin ast parsing
        with zipfile.ZipFile(temp_path, "r") as z:
            base_path = temp_path.replace(".zip", "")
            z.extractall(base_path)
            chunks = concurrent_parse(base_path)
            return {
                "name": zip.name,
                "content_type": zip.content_type,
                "size": zip.size,
                "num_chunks": len(chunks),
                "message": "Successfully parsed zip"
            }

@router.get("/")
def server_test():
    return "Server running correctly."


