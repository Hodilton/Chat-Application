from pydantic import BaseModel, Field
from typing import List

class ChatCreate(BaseModel):
    name: str = Field(..., example="My Chat")
    user_ids: List[int] = Field(..., min_items=2, example=[1, 2])
