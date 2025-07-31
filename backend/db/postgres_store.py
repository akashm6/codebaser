from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.models import Base, Chunk
from dotenv import load_dotenv
from typing import List, Dict
import hashlib
import os

load_dotenv()

DB_USER = os.getenv("DATABASE_USER") or 'postgres'
DB_HOST = os.getenv("DATABASE_HOST") or 'localhost'
DB_PORT = os.getenv("DATBASE_PORT") or 5432
DB_NAME = os.getenv("DATABASE_NAME") or 'codebaser_db_dev'

DATABASE_URL = os.getenv("DATABASE_CONN_STRING") or f"postgresql://{DB_USER}:@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def insert_chunk(chunk: dict):
    session = SessionLocal()
    chunk_id = get_chunk_id(chunk)

    db_chunk = Chunk(
        id=chunk_id,
        file_path = chunk.get("file_path", ''),
        start_line = chunk.get("start_line", None),
        end_line = chunk.get("end_line", None),
        type = chunk.get("type", None),
        summary = chunk.get("summary", "")
    )

    session.merge(db_chunk)
    session.commit()
    print("succesfully inserted")
    session.close()

def get_chunk_id(chunk: Dict) -> str:
    base = f"{chunk['file_path']}:{chunk['start_line']}-{chunk['end_line']}"
    return hashlib.sha256(base.encode()).hexdigest()

def get_chunks_by_ids(chunk_ids: List[str]) -> List[dict]:
    chunks = []
    session = SessionLocal()
    rows = session.query(Chunk).filter(Chunk.id.in_(chunk_ids)).all()
    session.close()

    for r in rows:
        c = {
        "chunk_id": r.id,
        "file_path": r.file_path,
        "start_line": r.start_line,
        "end_line": r.end_line,
        "type": r.type,
        "summary": r.summary,
        }
        chunks.append(c)

    return chunks

def create_tables():
    Base.metadata.create_all(engine)    

def test_conn():
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
            print("DB Connection Works.")
    except Exception as e:
        print("DB Connection Failed.")
        print(e)