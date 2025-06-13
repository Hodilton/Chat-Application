from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMemberOutput(BaseModel):
    id: int
    username: str
    email: str

class ChatOutput(BaseModel):
    chat_id: int
    name: str
    created_at: Optional[datetime]
    members: List[ChatMemberOutput]

class UserChatsOutput(BaseModel):
    user_id: int
    chats: List[ChatOutput]

class ChatCreateResponse(BaseModel):
    message: str
    chat_id: int

class ChatDeleteResponse(BaseModel):
    message: str
