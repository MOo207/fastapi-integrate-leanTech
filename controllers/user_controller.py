from schemas.schemas import SignupUser, User
from models.db import SessionLocal
from os import stat
from re import template
from urllib.request import Request
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from model_controller import lean_data_model_controller
from model_controller import user_model_controller
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import unquote as unquote

from utils import utils

templates = Jinja2Templates(directory="templates")


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

def render_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

async def signup_user(request: Request, db: Session = Depends(get_db)):
    try:
        error = None
        # Workaround for the fact that form not send json data
        form_body = await request.body()
        decoded_form_body = form_body.decode("utf-8")
        decoded_string = unquote(decoded_form_body)
        prepared = decoded_string.replace(
            "email=", "").replace("password=", "").split("&")
        email = prepared[0]
        password = prepared[1]
        db_user = user_model_controller.get_user_by_email(db, email=email)

        if db_user is not None:
             return templates.TemplateResponse("signup.html", {"request": request, "error": "User already exists"})
        else:
            created_user = user_model_controller.create_user(db=db, email=email, password=password)
            print(created_user)
            return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "error": e})


async def login(request: Request, db: Session = Depends(get_db)):
    try:
        error = None
        # Workaround for the fact that form not send json data
        form_body = await request.body()
        decoded_form_body = form_body.decode("utf-8")
        decoded_string = unquote(decoded_form_body)
        prepared = decoded_string.replace(
            "email=", "").replace("password=", "").split("&")
        email = prepared[0]
        password = prepared[1]
        db_user = user_model_controller.get_user_by_email(db, email=email)

        if db_user and utils.verify_password(password, db_user.password):
            lean_user = lean_data_model_controller.get_lean_user(db, user_id=db_user.id)
            if lean_user:
                entity_id = lean_user.entity_id
                if entity_id:
                    return templates.TemplateResponse("lean_home.html", {"request": request, "lean_user": lean_user})
                else:
                    return templates.TemplateResponse("lean_link.html", {"request": request, "customer_id": lean_user.customer_id})
            else: 
                return templates.TemplateResponse("create_customer.html", {"request": request, "user_id": db_user.id})
        else:
            if db_user is None:
                error = "User not found"
            elif not utils.verify_password(password, db_user.password):
                error = "Wrong password"
            return templates.TemplateResponse("login.html", {"request": request, "error": error, "user": db_user})

    except Exception as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": e})


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    try:
        return user_model_controller.update_user(db=db, user_id=user_id, user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


def delete_user(db: Session, user_id: int):
    try:
        return user_model_controller.delete_user(db=db, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
