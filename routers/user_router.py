import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Response
import requests
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from models.db import SessionLocal
from models.models import User
from models.schemas import UserCreate
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


@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_controller.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")
        else:
            return user_controller.create_user(db=db, user=user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)


@router.post('/login', response_class=HTMLResponse)
async def login(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    try:
        req_body = await request.body()
        print(req_body)
        email = user.email
        password = user.password
        error = None
        db_user = user_controller.get_user_by_email_and_password(db, email=email, password=password)
        if db_user:
            return templates.TemplateResponse("entity.html", {"error": error, "request": request, "data": user})
        else: 
            error = "Invalid email or password"
            return templates.TemplateResponse("login.html", {"request": request, "error": error}) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)