from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Chunk(Base):
    __tablename__ = 'chunk_table'

    id = Column(String, primary_key=True)
    file_path = Column(String)
    start_line = Column(Integer)
    end_line = Column(Integer)
    type = Column(Text)
    summary = Column(String)