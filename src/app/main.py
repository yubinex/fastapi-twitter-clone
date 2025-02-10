from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db_and_models.session import create_db_and_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    drop_tables()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"message": "hello world"}
