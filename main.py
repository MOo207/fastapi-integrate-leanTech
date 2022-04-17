from routers import lean_data_api_route, user_router
from models import models, db
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
import sys
sys.setrecursionlimit(1500)

load_dotenv()

# Binds all models to the database
models.Base.metadata.create_all(bind=db.engine)

models.Base

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(user_router.router, prefix="", tags=["Users Route"])
app.include_router(lean_data_api_route.router, prefix="/lean", tags=["Lean API Data Route"])

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True, debug=True, )
