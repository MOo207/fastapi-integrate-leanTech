from os import stat
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import models

from model_controller import user_model_controller
from fastapi.responses import JSONResponse


from models.db import SessionLocal

from schemas.schemas import User, UserCreate

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_users(db: Session = Depends(get_db)):
    try:
        users = user_model_controller.get_users(db=db)
        return users
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)

def get_user(db: Session, user_id: int):
    try:
        user = user_model_controller.get_user(db=db, user_id=user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_model_controller.get_user_by_email_and_password(db, email=user.email, password=user.password)
        if db_user is not None:
            raise HTTPException(
                status_code=400, detail="Email already registered")
        else:
            return user_model_controller.create_user(db=db, user=user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)

async def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_model_controller.get_user_by_email_and_password(db, email=user.email, password=user.password)
        if db_user:
            return db_user
        else: 
            return None
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)

def update_user(db: Session, user_id: int, user: UserCreate):
    try:
        return user_model_controller.update_user(db=db, user_id=user_id, user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

def delete_user(db: Session, user_id: int):
    try:
        return user_model_controller.delete_user(db=db, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)