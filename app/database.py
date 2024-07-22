from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_URL = "postgresql://postgres:root@localhost/xpayback"
MONGO_URL = "mongodb://localhost:27017"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

mongodb_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongodb_client["xpayback"]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
