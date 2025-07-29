from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

final_frontend_url = os.getenv("FINAL_FRONTEND_URL") or None

origins = [
    "http://localhost:3000",
    final_frontend_url,
] if final_frontend_url else ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


