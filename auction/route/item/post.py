import aiohttp
import datetime
from auction.utility.validate import validate_schema


@validate_schema({
    "type": "object",
    "properties": {
        "auction_end_date": {"type": "number"},
    },
    "required": ["auction_end_date"]
})
async def post_item(request):
    body = await request.json()
    pool = request.app['connection_pool']
    end_date = datetime.datetime.utcfromtimestamp(body['auction_end_date'])

    async with pool.acquire() as connection:
        result = await connection.fetchval('''
            INSERT INTO item(auction_end_date) VALUES ($1) RETURNING id
        ''', end_date)

        return aiohttp.web.json_response(result)
