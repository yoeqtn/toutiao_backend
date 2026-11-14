from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routers
from utils.exception_handlers import register_exception_handlers
from contextlib import asynccontextmanager
from config.db_conf import async_engine
from models.news import Base as NewsBase
from models.users import Base as UsersBase
from models.history import Base as HistoryBase
from models.favorite import Base as FavoriteBase

# 各模型文件使用独立的 DeclarativeBase，需要按外键依赖顺序逐个建表
MODEL_BASES = (NewsBase, UsersBase, HistoryBase, FavoriteBase)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        for base in MODEL_BASES:
            await conn.run_sync(base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# 允许本地前端开发服务器跨域访问（Vite 默认 5173 端口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
register_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂载路由/注册路由
app.include_router(routers.router)
