from fastapi import APIRouter
from .routes import users, chats, messages, reset

router = APIRouter()
router.include_router(reset.router, prefix="/admin", tags=["Admin"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(chats.router, prefix="/chats", tags=["Chats"])
router.include_router(messages.router, prefix="/messages", tags=["Messages"])