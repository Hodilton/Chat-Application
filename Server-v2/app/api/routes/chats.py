from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.input.chats import ChatCreate
from app.schemas.output.chats import ChatOutput, UserChatsOutput, ChatCreateResponse, ChatDeleteResponse, \
    ChatMemberOutput
from data_base import Database, DatabaseError

router = APIRouter()


async def get_chats_repo():
    async with Database() as db:
        yield db.get_repository("chats"), db.get_repository("chat_members")


@router.post("/", response_model=ChatCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(data: ChatCreate, repos=Depends(get_chats_repo)):
    chats_repo, members_repo = repos
    try:
        if not data.name or len(data.user_ids) < 2:
            raise HTTPException(status_code=400, detail="Chat name and at least 2 user IDs are required")

        chat_id = await chats_repo.insert((data.name,))

        for user_id in data.user_ids:
            await members_repo.insert((chat_id, user_id))

        return ChatCreateResponse(message="Chat created", chat_id=chat_id)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.delete("/{chat_id}", response_model=ChatDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_chat(chat_id: int, repos=Depends(get_chats_repo)):
    chats_repo, _ = repos
    try:
        await chats_repo.delete("by_id", (chat_id,))
        return ChatDeleteResponse(message="Chat deleted")

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@router.post("/{chat_id}/members", response_model=ChatCreateResponse, status_code=status.HTTP_200_OK)
async def add_user_to_chat(chat_id: int, user_id: int, repos=Depends(get_chats_repo)):
    chats_repo, members_repo = repos
    try:
        chat = await chats_repo.fetch_one("by_id", (chat_id,))
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        existing_member = await members_repo.fetch_one(
            "member_by_chat_and_user",
            (chat_id, user_id)
        )
        if existing_member:
            raise HTTPException(
                status_code=400,
                detail="User already in this chat"
            )

        await members_repo.insert((chat_id, user_id))

        return ChatCreateResponse(
            message="User added to chat",
            chat_id=chat_id
        )

    except DatabaseError as e:
        raise HTTPException( status_code=500, detail=f"Internal Server Error: {e}")

@router.get("/", response_model=UserChatsOutput, status_code=status.HTTP_200_OK)
async def get_user_chats(user_id: int, repos=Depends(get_chats_repo)):
    chats_repo, members_repo = repos
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing required user fields")

        chat_ids = await members_repo.fetch_many("chats_by_user", (user_id,))
        if not chat_ids:
            return UserChatsOutput(user_id=user_id, chats=[])

        chats = []
        for row in chat_ids:
            chat = await chats_repo.fetch_one("by_id", (row.get("chat_id"),))
            if not chat:
                continue

            members = await members_repo.fetch_many("members_by_chat", (row.get("chat_id"),))

            chats.append(ChatOutput(
                chat_id=chat["id"],
                name=chat["name"],
                created_at=chat["created_at"],
                members=[
                    ChatMemberOutput(
                        id=m["id"],
                        username=m["username"],
                        email=m["email"]
                    ) for m in members
                ]
            ))

        return UserChatsOutput(user_id=user_id, chats=chats)

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
