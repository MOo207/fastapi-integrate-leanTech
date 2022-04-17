from fastapi import Depends
from sqlalchemy.orm import Session
from models.db import SessionLocal

from schemas import schemas
from models import models
from utils import utils

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_lean_user(db: Session, user_id: int, user: dict):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.query(models.User).filter(models.User.id == user_id).update(user)
        db.commit()
        return user
    else:
        return None

def get_lean_user(db: Session, user_id: int):
    return db.query(models.LeanUser).filter(models.LeanUser.user_id == user_id).first()

def get_lean_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LeanUser).offset(skip).limit(limit).all()

def create_lean_customer(db: Session, user_id: int, response: dict):
    db_user = get_user(user_id=user_id, db=db)
    if db_user:
        lean_user = get_lean_user(db, user_id)
        if lean_user:
            response["message"] = "User already has a Lean account"
            return response
        else:
            db_lean = models.LeanUser(app_user_id= response["app_user_id"], customer_id= response["customer_id"], user_id=user_id)
            print("----------------"+str(db_lean))
            db.add(db_lean)
            db.commit()
            return db_lean
       
    else:
        return None

def link_lean_user(db: Session,user_id: int,  lean: schemas.LeanUserLink):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_lean = models.LeanUser(**lean.dict(), user_id=user_id)
        db.add(db_lean)
        db.commit()
        return db_lean
    else:
        return None

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_lean_user_by_customer_id(db: Session, customer_id: int):
    return db.query(models.LeanUser).filter(models.LeanUser.customer_id == customer_id).first()

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.query(models.User).filter(models.User.id == user_id).update(user.dict())
        db.commit()
        return user
    else:
        return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return "User deleted"


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
