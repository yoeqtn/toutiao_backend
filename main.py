from fastapi import FastAPI
import routers
from utils.exception_handlers import register_exception_handlers
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from config.db_conf import async_engine

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# 注册异常处理器
register_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂载路由/注册路由
app.include_router(routers.router)
