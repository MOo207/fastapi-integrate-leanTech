from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.db import SessionLocal
from models.models import User
from schemas.schemas import UserCreate
from controllers import user_controller
from model_controller import user_model_controller
templates = Jinja2Templates(directory="templates")

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/login')
async def login(request: Request, db: Session = Depends(get_db)):
    return await user_controller.login(request=request, db=db)


@router.get("/signup")
def render_signup(request: Request):
    return user_controller.render_signup(request)

@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    return await user_controller.signup_user(request=request,db=db)


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return user_controller.get_users(db=db)


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_user(db=db, user_id=user_id)


@router.put('/update/{user_id}')
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return await user_controller.update_user(user_id=user_id, db=db, user=user)


@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return await user_controller.delete_user(user=user_id, db=db)
