from fastapi import APIRouter

from routers import agent, favorite, history, news, users

router = APIRouter()

router.include_router(agent.router)
router.include_router(favorite.router)
router.include_router(users.router)
router.include_router(history.router)
router.include_router(news.router)