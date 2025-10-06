from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api import api_router
from .database import create_db_and_tables

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(api_router)
