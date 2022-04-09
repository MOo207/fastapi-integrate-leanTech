import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import sys
sys.setrecursionlimit(1500)

from routers import lean_data_api_route, user_router    
from dotenv import load_dotenv
load_dotenv()

from models import models, db
# Binds all models to the database
models.Base.metadata.create_all(bind=db.engine)

models.Base

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(user_router.router, prefix="", tags=["Users Route"])
app.include_router(lean_data_api_route.router, prefix="/lean", tags=["Lean API Data Route"])