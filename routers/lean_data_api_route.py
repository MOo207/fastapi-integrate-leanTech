import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
import requests
from controllers import lean_data_api_controller

from models.db import SessionLocal
from schemas.schemas import LeanUserLink
from sqlalchemy.orm import Session
from schemas import schemas
from models import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/data_home")
def fetch_identity(request: Request):
    return lean_data_api_controller.render_data_home(request)

@router.post('/create_lean_customer/{user_id}')
async def create_lean_customer_post(user_id: int, request: Request, db: Session = Depends(get_db),):
    return await lean_data_api_controller.create_lean_customer_post(request=request, user_id=user_id,db=db)

@router.get('/get_lean_customers')
def get_lean_customers(db: Session = Depends(get_db)):
    return lean_data_api_controller.get_lean_customers(db)

@router.get("/lean_link")
def render_lean_link(request: Request):
    return lean_data_api_controller.render_lean_link(request)

@router.post("/hook_handler")
async def hook_handler(request: Request):
    return await lean_data_api_controller.hook_handler(request)

@router.get("/get_lean_user_by_customer_id/{customer_id}")
def get_lean_user_by_customer_id(customer_id: str, db: Session = Depends(get_db)):
    return lean_data_api_controller.get_lean_user_by_customer_id(db=db, customer_id=customer_id)

@router.post("/get_identity")
async def get_identity(request: Request):
    return await lean_data_api_controller.get_identity(request)


@router.post("/get_accounts")
async def get_accounts(request: Request):
    return await lean_data_api_controller.get_accounts(request)

@router.post("/get_balance")
async def get_balance(request: Request):
    return lean_data_api_controller.get_balance(request)