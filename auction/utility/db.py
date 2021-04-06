import os
import asyncpg
import asyncio


async def getConnectionPool():
    while True:
        try:
            result = await asyncpg.create_pool(dsn=os.getenv('DB_URL'))
            return result
        except:
            await asyncio.sleep(2)
