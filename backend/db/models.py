from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Chunk(Base):
    __tablename__ = 'chunk_table'

    id = Column(String, primary_key=True)
    file_path = Column(String)
    start_line = Column(Integer)
    end_line = Column(Integer)
    type = Column(Text)
    summary = Column(String)
    
class User(Base):
    
    __tablename__ = "users_table"
    
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    