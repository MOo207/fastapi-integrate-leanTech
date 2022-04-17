import os
import uuid
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from controllers.user_controller import get_user
from model_controller import lean_data_model_controller
import requests
from models.db import SessionLocal




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_lean_customer(db: Session = Depends(get_db),):
    try:
        lean_app_token = os.getenv("LEAN_APP_TOKEN")
        headers = {'Content-Type': 'application/json',
                'lean-app-token': lean_app_token, }
        uid = uuid.uuid4()
        body = {"app_user_id": str(uid)}
        url = "https://sandbox.leantech.me/customers/v1"
        lean_request = requests.post(url, headers=headers, json=body)
        print(lean_request.status_code)
        if lean_request.status_code == 200:
            response = lean_request.json()
            print(response)
            db_lean = lean_data_model_controller.create_lean_customer(db=db, response=response)
        return db_lean
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)

def get_lean_customers(db: Session = Depends(get_db)):
    try:
        users = lean_data_model_controller.get_lean_customers(db)
        return users
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=e)

templates = Jinja2Templates(directory="templates")

def render_lean_link(customer_id: str, request: Request):
    return templates.TemplateResponse("lean_link.html", {"request": request, "customer_id": customer_id,})

async def entity_hook_handler(request: Request):
    body = await request.json()
    hook_type = body.get("type")
    customer_id = body.get("payload").get("customer_id")
    response = requests.get(url="http://localhost:8000/lean/get_lean_user_by_customer_id/" + customer_id)
    if response.status_code == 200:
        if hook_type == "entity.created":
            entity_id = body.get("payload").get("id")
            print(entity_id)
            return {"entity_id": entity_id}
        elif hook_type == "payment_source.beneficiary.created":
            payment_source_id = body.get("payload").get("payment_source_id")
            print(payment_source_id)
            payment_destination_id = body.get("payload").get("payment_destination_id")
            print(payment_destination_id)
            return {"payment_source_id": payment_source_id, "payment_destination_id": payment_destination_id}
        elif hook_type == "payment_source.created":
            bank_identifier = body.get("payload").get("bank_identifier")
            print(bank_identifier)
            return {"bank_identifier": bank_identifier}
        else:
            return HTTPException(status_code=400, detail="Invalid hook type")
    else:
        return HTTPException(status_code=400, detail="Invalid customer id")

def get_lean_user_by_customer_id(customer_id: str, db: Session = Depends(get_db)):
    lean_user = lean_data_model_controller.get_lean_user_by_customer_id(db=db, customer_id=customer_id)
    return lean_user

def create_lean_customer_get(request: Request):
    return templates.TemplateResponse("create_customer.html", {"request": request})

async def create_lean_customer_post(user_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        lean_app_token = os.getenv("LEAN_APP_TOKEN")
        headers = {'Content-Type': 'application/json',
                   'lean-app-token': lean_app_token, }
        uid = uuid.uuid4()
        body = {"app_user_id": str(uid)}
        url = "https://sandbox.leantech.me/customers/v1"
        lean_request = requests.post(url, headers=headers, json=body)
        print(lean_request.status_code)
        if lean_request.status_code == 200:
            response = lean_request.json()
            # insert into db
            db_lean = lean_data_model_controller.create_lean_customer(db=db, user_id=user_id, response=response)
            return templates.TemplateResponse("lean_link.html", {"request": request, "customer_id": db_lean.customer_id,})
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

async def fetch_identity(request: Request):
    try:
        body = await request.json()
        entity_id = body.get("entity_id")
        print(entity_id)
        lean_app_token = os.getenv("LEAN_APP_TOKEN")
        url = "https://sandbox.leantech.me/data/v1/identity"
        headers = {'Content-Type': 'application/json',
                   'lean-app-token': lean_app_token, }
        body = {"entity_id": entity_id, }
        identity_request = requests.post(url, headers=headers, json=body)
        print(identity_request.status_code)
        if identity_request.status_code == 200:
            response = identity_request.json()
            return JSONResponse(content= response, status_code=200)
        else:
            HTTPException(status_code=400, detail="identity_request failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

async def fetch_accounts(request: Request):
    try:
        req_body = await request.json()
        entity_id = req_body.get("entity_id")
        lean_app_token = os.getenv("LEAN_APP_TOKEN")
        print(lean_app_token)
        url = "https://sandbox.leantech.me/data/v1/accounts"
        headers = {'Content-Type': 'application/json',
                   'lean-app-token': lean_app_token, }
        body = {"entity_id": entity_id, }
        identity_request = requests.post(url, headers=headers, json=body)
        if identity_request.status_code == 200:
            response = identity_request.json()
            return JSONResponse(content= response, status_code=200)
        else:
            HTTPException(status_code=400, detail="identity_request failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


async def fetch_balance(request: Request):
    try:
        req_body = await request.json()
        entity_id = request.session.get("entity_id", None)
        print(entity_id)
        account_id = req_body.get("account_id")
        lean_app_token = os.getenv("LEAN_APP_TOKEN")
        print(lean_app_token)
        url = "https://sandbox.leantech.me/data/v1/balance"
        headers = {'Content-Type': 'application/json',
                   'lean-app-token': lean_app_token, }
        body = {"entity_id": entity_id,
                "account_id": account_id, }
        identity_request = requests.post(url, headers=headers, json=body)
        if identity_request.status_code == 200:
            response = identity_request.json()
            return JSONResponse(content= response, status_code=200)
        else:
            HTTPException(status_code=400, detail="identity_request failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)