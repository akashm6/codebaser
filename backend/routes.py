from fastapi import APIRouter, Query
from dotenv import load_dotenv
from s3_utils import generate_presigned_url
import os

router = APIRouter()

@router.get("/generate-presigned-url")
def get_presigned_url(filename: str = Query(...), content_type: str = Query(...)):
    return generate_presigned_url(filename, content_type)

@router.get("/")
def server_test():
    return "Server running correctly."


