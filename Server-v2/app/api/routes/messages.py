from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.input.messages import MessageCreate
from app.schemas.output.messages import (
    MessageCreateResponse, MessageDeleteResponse,
    ChatMessagesOutput, MessageOutput, MessageSenderOutput
)
from data_base import Database, DatabaseError

router = APIRouter()

async def get_messages_repo():
    async with Database() as db:
        yield (
            db.get_repository("messages"),
            db.get_repository("chats"),
            db.get_repository("users")
        )


@router.post("/", response_model=MessageCreateResponse, status_code=status.HTTP_201_CREATED)
async def send_message(data: MessageCreate, repos=Depends(get_messages_repo)):
    messages_repo, chats_repo, users_repo = repos
    try:
        if not data.chat_id or not data.sender_id or not data.content.strip():
            raise HTTPException(status_code=400, detail="Missing required message fields")

        chat = await chats_repo.fetch_one("by_id", (data.chat_id,))
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        sender = await users_repo.fetch_one("by_id", (data.sender_id,))
        if not sender:
            raise HTTPException(status_code=404, detail="Sender not found")

        message_id = await messages_repo.insert((data.chat_id, data.sender_id, data.content.strip()))
        message = await messages_repo.fetch_one("by_id", (message_id,))

        return MessageCreateResponse(
            id=message["id"],
            chat_id=message["chat_id"],
            content=message["content"],
            sent_at=message["sent_at"].strftime("%Y-%m-%d %H:%M:%S"),
            sender=MessageSenderOutput(
                id=sender["id"],
                username=sender["username"],
                email=sender["email"]
            )
        )

    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.delete("/{message_id}", response_model=MessageDeleteResponse, status_code=status.HTTP_200_OK)
async def delete_message(message_id: int, repos=Depends(get_messages_repo)):
    messages_repo, _, _ = repos
    try:
        await messages_repo.delete("by_id", (message_id,))
        return MessageDeleteResponse(message="Message deleted")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/{chat_id}", response_model=ChatMessagesOutput, status_code=status.HTTP_200_OK)
async def get_chat_messages(chat_id: int, repos=Depends(get_messages_repo)):
    messages_repo, _, _ = repos
    try:
        messages = await messages_repo.fetch_many("by_chat", (chat_id,))
        if not messages:
            return ChatMessagesOutput(chat_id=chat_id, count=0, messages=[])
        result = [
            MessageOutput(
                id=msg["id"],
                chat_id=chat_id,
                content=msg["content"],
                sent_at=msg["sent_at"].strftime("%Y-%m-%d %H:%M:%S"),
                sender=MessageSenderOutput(
                    id=msg["u.id"],
                    username=msg["username"]
                )
            )
            for msg in messages
        ]
        return ChatMessagesOutput(chat_id=chat_id, count=len(result), messages=result)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@router.get("/{chat_id}/new", response_model=ChatMessagesOutput, status_code=status.HTTP_200_OK)
async def get_new_messages(chat_id: int, last_id: int = Query(0), repos=Depends(get_messages_repo)):
    messages_repo, _, _ = repos
    try:
        new_messages = await messages_repo.fetch_many("new_messages", (chat_id, last_id))
        if not new_messages:
            return ChatMessagesOutput(chat_id=chat_id, count=0, messages=[])
        result = [
            MessageOutput(
                id=msg["id"],
                chat_id=chat_id,
                content=msg["content"],
                sent_at=msg["sent_at"].strftime("%Y-%m-%d %H:%M:%S"),
                sender=MessageSenderOutput(
                    id=msg["u.id"],
                    username=msg["username"]
                )
            )
            for msg in new_messages
        ]
        return ChatMessagesOutput(chat_id=chat_id, count=len(result), messages=result)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
