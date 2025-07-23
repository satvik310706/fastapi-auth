import os
from dotenv import load_dotenv
from fastapi import FastAPI
from auth.routes import router as auth_router
from routers.routes import router

load_dotenv()

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(router, prefix="/auth", tags=["dashboard"])
