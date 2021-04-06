import asyncio
from auction.utility.db import getConnectionPool


async def main():
    pool = await getConnectionPool()

    while True:
        async with pool.acquire() as connection:
            bids = await connection.fetch('''
                SELECT item.*
                FROM item
                WHERE item.auction_end_date > now()
            ''')

        await asyncio.sleep(5)


asyncio.get_event_loop().run_until_complete(main())
