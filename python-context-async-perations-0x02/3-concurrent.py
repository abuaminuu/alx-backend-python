import asyncio
import aiosqlite


# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users_db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            await results = cursor.fetchall()
            print("all users")
            for user in results:
                print(user)
            return results


# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users_db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("users older than 40")
            for user in results:
                print(user)
            return results
            

# Run both functions concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# start the async event loop and runs your concurrent queries.
if __name__ == "__main__":
    asyncio.run(fetch_concurrently)
