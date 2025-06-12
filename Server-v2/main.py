import asyncio
from log_manager import LogManager
from data_base import Database

async def run():
    async with Database() as db:
        users_repo = db.get_repository("users")

        # await users_repo.create()
        # await users_repo.insert(("alice", "alice@example.com", "hashed_pw"))
        # user = await users_repo.fetch_one("fetch.by_username", ("alice",))
        # print("Fetched user:", user)

        # await users_repo.update(("alice_updated", "alice@new.com", "new_pw"), (user["id"],))
        # all_users = await users_repo.fetch_all("fetch.all")
        # print("All users:", all_users)

        # await users_repo.delete("by_id", (user["id"],))
        # await users_repo.drop()

        await Database.close_instance()

if __name__ == "__main__":
    log_manager = LogManager("config/logging_config.json")
    log_manager.setup_logging()

    asyncio.run(run())