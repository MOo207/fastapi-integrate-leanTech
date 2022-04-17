import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from matplotlib.style import use
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

@router.post('/create_lean_customer/{user_id}')
async def create_lean_customer_post(user_id: int, request: Request, db: Session = Depends(get_db),):
    return await lean_data_api_controller.create_lean_customer_post(request=request, user_id=user_id,db=db)

@router.get('/get_lean_customers')
def get_lean_customers(db: Session = Depends(get_db)):
    return lean_data_api_controller.get_lean_customers(db)

@router.get("/lean_link")
def render_lean_link(request: Request):
    return lean_data_api_controller.render_lean_link(request)

@router.post("/entity_hook_handler")
async def entity_hook_handler(request: Request):
    return await lean_data_api_controller.entity_hook_handler(request)

@router.get("/get_lean_user_by_customer_id/{customer_id}")
def get_lean_user_by_customer_id(customer_id: str, db: Session = Depends(get_db)):
    return lean_data_api_controller.get_lean_user_by_customer_id(db=db, customer_id=customer_id)

@router.post("/fetch_identity")
async def fetch_identity(request: Request):
    return await lean_data_api_controller.fetch_identity(request)


@router.post("/fetch_accounts")
async def fetch_accounts(request: Request):
    return lean_data_api_controller.fetch_accounts(request)

@router.post("/fetch_balance")
async def fetch_balance(request: Request):
    return lean_data_api_controller.fetch_balance(request)