import aiohttp
import time

from auction.utility.validate import validate_schema


@validate_schema({
    "type": "object",
    "properties": {
        "amount": {"type": "number", "exclusiveMinimum": 0},
        "user_id": {"type": "number"},
    },
    "required": ["amount", "user_id"]
})
async def post_bid(request):
    item_id = int(request.match_info.get('id'))
    body = await request.json()
    pool = request.app['connection_pool']

    async with pool.acquire() as connection:
        item_record = await connection.fetchrow('''
            SELECT *
            FROM item
            WHERE item.id = $1
            LIMIT 1
        ''', item_id)

        if not item_record:
            raise aiohttp.web.HTTPNotFound()

        if item_record['auction_end_date'].timestamp() < time.time():
            raise aiohttp.web.HTTPBadRequest(
                text=f'Auction has expired')

        highest_bid_amount = await connection.fetchval('''
            SELECT bid.amount
            FROM bid
            WHERE bid.item_id = $1
            ORDER BY bid.amount DESC
            LIMIT 1
        ''', item_id)

        if highest_bid_amount and highest_bid_amount >= body['amount']:
            raise aiohttp.web.HTTPBadRequest(
                text=f'bid amount must be greater than {highest_bid_amount}')

        await connection.execute('''
            INSERT INTO bid(amount, user_id, item_id) VALUES ($1, $2, $3)
        ''', body['amount'], body['user_id'], item_id)

        return aiohttp.web.Response()
