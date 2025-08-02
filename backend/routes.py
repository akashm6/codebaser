from embedding.summarize import synthesize_answer, embed_and_summarize_chunk
from parallel_processing.multiprocessor import concurrent_parse
from db.chroma_store import search_codebase, store_embedding
from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Query, Header, Depends
from s3_utils import generate_presigned_url, s3
from fastapi.responses import RedirectResponse
from db.postgres_store import insert_chunk, SessionLocal
from db.models import User
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel
import tempfile
import subprocess
import zipfile
import shutil
import httpx
import uuid
import jwt
import os

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
FINAL_FRONTEND_URL = os.getenv("FINAL_FRONTEND_URL")

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
    
class GitHubRepoRequest(BaseModel):
    url: str

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
    
@router.post("/github-process")
def github_process(
    repo: GitHubRepoRequest,
    user_id: str = Depends(get_current_user),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    github_token = payload.get("github_token")  
    if not github_token:
        raise HTTPException(status_code=401, detail="Missing GitHub token")

    repo_url = repo.url
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    repo_path = repo_url.replace("https://github.com/", "")
    zip_id = str(uuid.uuid4())
    temp_dir = f"/tmp/{zip_id}"
    zip_path = f"/tmp/{zip_id}.zip"

    authed_url = f"https://{github_token}:x-oauth-basic@github.com/{repo_path}"
    try:
        subprocess.run(["git", "clone", authed_url, temp_dir], check=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Git clone failed (private or invalid repo)")

    shutil.make_archive(temp_dir, 'zip', temp_dir)

    with zipfile.ZipFile(f"{temp_dir}.zip", "r") as z:
        extract_path = temp_dir + "_unzipped"
        z.extractall(extract_path)
        chunks = concurrent_parse(extract_path)

        for chunk in chunks:
            chunk["user_id"] = user_id
            enriched = embed_and_summarize_chunk(chunk)
            insert_chunk(enriched)
            store_embedding(enriched)

    shutil.rmtree(temp_dir, ignore_errors=True)
    shutil.rmtree(extract_path, ignore_errors=True)
    os.remove(zip_path)

    return {
        "repo": repo_url,
        "num_chunks": len(chunks),
        "message": "Repo successfully processed"
    }


@router.post("/zip-processing")
def process_zip(zip: ZipFileModel, user_id: str = Depends(get_current_user)):
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
    session = SessionLocal()
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
        github_id = str(user_data["id"])
        account = user_data.get("html_url")
        
        user = session.query(User).filter(User.github_id == github_id).first()
        
        if not user:
            user = User(github_id=github_id, email=account)
            session.add(user)
            session.commit()
            session.close()

        payload = {
            "sub": github_id,
            "exp": datetime.utcnow() + timedelta(hours=12),
            "github_token": access_token,
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        redirect_url = f"{FINAL_FRONTEND_URL}/auth-success?token={token}"
        return RedirectResponse(url=redirect_url)
       
@router.get("/")
def server_test():
    return "Server running correctly."


