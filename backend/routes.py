from fastapi import APIRouter, Query
from dotenv import load_dotenv
from s3_utils import generate_presigned_url
from pydantic import BaseModel
import os

class ZipFileModel(BaseModel):
    name: str
    content_type: str
    size: int

router = APIRouter()

@router.get("/generate-presigned-url")
def get_presigned_url(filename: str = Query(...), content_type: str = Query(...)):
    return generate_presigned_url(filename, content_type)

@router.post("/zip-processing")
def process_zip(zip: ZipFileModel):

    name = zip.name
    content_type = zip.content_type
    size = zip.size
    return {"name": name, "content_type": content_type, "size": size, "message": "hello!!!"}


@router.get("/")
def server_test():
    return "Server running correctly."


