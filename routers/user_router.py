import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Response
import requests
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from models.db import SessionLocal
from models.models import User
from schemas.schemas import UserCreate
from controllers import user_controller

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


templates = Jinja2Templates(directory="templates")

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post('/login', response_class=HTMLResponse)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    return await user_controller.login(user=user, db=db)

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.signup_user(user=user, db=db)


@router.get("/users")
def signup(db: Session = Depends(get_db)):
    return user_controller.get_users(db=db)


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_user(db=db, user_id=user_id)




@router.put('/update/{user_id}', response_class=HTMLResponse)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return await user_controller.update_user(user_id=user_id, db=db, user=user)


@router.delete('/delete/{user_id}', response_class=HTMLResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return await user_controller.delete_user(user=user_id, db=db)
