from fastapi import APIRouter
from data_base import Database

router = APIRouter()

@router.post("/")
async def reset_database():
    try:
        async with Database() as db:
            await Database.reset()
        return {"detail": "Database reset successful"}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))