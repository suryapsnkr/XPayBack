from sqlalchemy.orm import Session
from . import models
from . import schemas
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=fake_hashed_password.decode('utf-8')
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_profile(mongodb: AsyncIOMotorClient, user_id: int, profile):
    collection = mongodb["profiles"]
    profile_doc = {
        "user_id": user_id,
        "profile_picture": profile
    }
    result = await collection.insert_one(profile_doc)
    return result.inserted_id

async def get_profile(mongodb: AsyncIOMotorClient, user_id: int):
    collection = mongodb["profiles"]
    profile = await collection.find_one({"user_id": user_id})
    return profile
