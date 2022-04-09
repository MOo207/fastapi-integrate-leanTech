from fastapi import APIRouter, Request
from controllers import lean_data_api_controller

router = APIRouter()

@router.get('/create_lean_customer')
def create_lean_customer():
    return lean_data_api_controller.create_lean_customer()

@router.get("/entity_frontend")
def render_entity_html(request: Request):
    return lean_data_api_controller.render_entity_html(request)

@router.post("/entity_hook_handler")
async def entity_hook_handler(request: Request):
    return await lean_data_api_controller.entity_hook_handler(request)

@router.post("/fetch_identity")
async def fetch_identity(request: Request):
    return await lean_data_api_controller.fetch_identity(request)


@router.post("/fetch_accounts")
async def fetch_accounts(request: Request):
    return lean_data_api_controller.fetch_accounts(request)

@router.post("/fetch_balance")
async def fetch_balance(request: Request):
    return lean_data_api_controller.fetch_balance(request)