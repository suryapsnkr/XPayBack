from fastapi import FastAPI, Depends, HTTPException,File, UploadFile
from sqlalchemy.orm import Session
import shutil
from . import crud, models
from . import schemas
from .database import engine, get_db, mongodb

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/register/", response_model=schemas.UserInDB)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email, phone = user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Email or Phone already registered")
    db_user = crud.create_user(db=db, user=user)
    return db_user

@app.post("/profile/{user_id}")
async def create_user_profile(user_id: int, file: UploadFile, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        profile = await crud.get_profile(mongodb, user_id)
        if profile:
            raise HTTPException(status_code=404, detail="Profile already exists")
        else:
            profile = "app/propics/"+file.filename
            with open(profile, 'wb') as f:
                shutil.copyfileobj(file.file, f)
            profile_id = await crud.create_profile(mongodb, user_id, profile)
            return {"profile_id": user_id, "profile_picture": profile}

@app.get("/user/{user_id}", response_model=schemas.UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/profile/{user_id}", response_model=schemas.Profile)
async def read_profile(user_id: int):
    profile = await crud.get_profile(mongodb, user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.get("/")
async def home_page():
    raise HTTPException(status_code=200, detail="Please visit on http://127.0.0.1:8000/docs")
