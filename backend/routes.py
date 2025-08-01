from embedding.summarize import synthesize_answer, embed_and_summarize_chunk
from parallel_processing.multiprocessor import concurrent_parse
from db.chroma_store import search_codebase, store_embedding
from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Query, Header, Depends
from s3_utils import generate_presigned_url, s3
from fastapi.responses import RedirectResponse
from db.postgres_store import insert_chunk
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel
import tempfile
import zipfile
import httpx
import jwt
import os

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET")

class ZipFileModel(BaseModel):
    s3_key: str
    name: str
    content_type: str
    size: int

class UserToken(BaseModel):
    access_token: str
    token_type: str

class AskRequest(BaseModel):
    query: str

router = APIRouter()
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@router.get("/generate-presigned-url")
def get_presigned_url(filename: str = Query(...), content_type: str = Query(...)):
    return generate_presigned_url(filename, content_type)

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/zip-processing")
def process_zip(zip: ZipFileModel, user_id: str = Depends(get_current_user)):
    
    print("Uploading as user_id:", user_id)

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
            
            for chunk in chunks:
                chunk["user_id"] = user_id
                enriched = embed_and_summarize_chunk(chunk)
                insert_chunk(enriched)
                store_embedding(enriched)
                
            return {
                "name": zip.name,
                "content_type": zip.content_type,
                "size": zip.size,
                "num_chunks": len(chunks),
                "message": "Successfully parsed zip"
            }

@router.post("/ask")
def ask_question(req: AskRequest, user_id: str = Depends(get_current_user)):
    query = req.query
    top_chunks = search_codebase(query, user_id=user_id, k = 5) 
    answer = synthesize_answer(query, top_chunks)
    return {
        "answer": answer,
        "chunks": top_chunks,
    }

@router.get("/auth/github/login")
def github_login():
    return RedirectResponse(
        url=f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=read:user"
    )

@router.get("/auth/github/callback")
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
        )
        token_data = res.json()
        access_token = token_data["access_token"]

        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_res.json()
        user_id = str(user_data["id"]) 

        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=7),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        redirect_url = f"http://localhost:3000/auth-success?token={token}"
        return RedirectResponse(url=redirect_url)
       
@router.get("/")
def server_test():
    return "Server running correctly."


