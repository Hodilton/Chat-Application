from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.input.users import UserCreate, UserLogin
from app.schemas.output.users import UserOutput
from data_base import Database, DatabaseError

router = APIRouter()

async def get_users_repo():
    async with Database() as db:
        yield db.get_repository("users")

@router.post("/register", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, repo=Depends(get_users_repo)):
    try:
        existing_user = await repo.fetch_one("by_username", (user.username,))
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        existing_email = await repo.fetch_one("by_email", (user.email,))
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        await repo.insert((user.username, user.email, user.password))
        new_user = await repo.fetch_one("by_username", (user.username,))

        return UserOutput(**new_user)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.post("/login", response_model=UserOutput)
async def login(credentials: UserLogin, repo=Depends(get_users_repo)):
    try:
        user = await repo.fetch_one("by_email", (credentials.email,))
        if not user or credentials.password != user["password_hash"]:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return UserOutput(**user)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.get("/", response_model=list[UserOutput])
async def get_all_users(repo=Depends(get_users_repo)):
    try:
        users = await repo.fetch_many("all")
        return [UserOutput(**u) for u in users]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.get("/{user_id}", response_model=UserOutput)
async def get_user(user_id: int, repo=Depends(get_users_repo)):
    try:
        user = await repo.fetch_one("by_id", (user_id,))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOutput(**user)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.get("/exclude/{exclude_id}", response_model=list[UserOutput])
async def get_users_exclude(exclude_id: int, repo=Depends(get_users_repo)):
    try:
        users = await repo.fetch_many("all_except", (exclude_id,))
        return [UserOutput(**u) for u in users]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
