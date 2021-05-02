import asyncio
from auction.utility.db import getConnectionPool


async def process_next_item(connection):
    def getNextItem():
        return connection.fetchrow('''
            SELECT   item.*
            FROM     item
            WHERE    item.auction_end_date < now()
            AND      item.highest_bidder IS NULL
            ORDER BY item.auction_end_date ASC
            LIMIT    1
        ''')

    item = await getNextItem()

    while item:
        highest_bid = await connection.fetchrow('''
            SELECT *
            FROM bid
            WHERE bid.item_id = $1
            ORDER BY bid.amount DESC
        ''', item['id'])

        highest_bidder = highest_bid['user_id'] if highest_bid else -1

        await connection.execute('''
            UPDATE item SET
            highest_bidder = $2
            WHERE item.id = $1
        ''', item['id'], highest_bidder)

        item = await getNextItem()


async def main():
    pool = await getConnectionPool()

    async with pool.acquire() as connection:
        await process_next_item(connection)


asyncio.get_event_loop().run_until_complete(main())
