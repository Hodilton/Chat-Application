from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
