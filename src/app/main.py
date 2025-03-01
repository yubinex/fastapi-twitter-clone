from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db_and_models.session import create_db_and_tables, drop_tables
from app.routers.followers import router as follower_router
from app.routers.likes import router as like_router
from app.routers.posts import router as post_router
from app.routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # delete DB automatically (for better dev experience)
    drop_tables()


app = FastAPI(lifespan=lifespan)

app.include_router(follower_router)
app.include_router(like_router)
app.include_router(post_router)
app.include_router(user_router)
