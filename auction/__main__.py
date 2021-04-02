import os
import asyncio
from aiohttp import web
from tortoise import Tortoise, fields, run_async

from auction.route.bid.post import post_bid
from auction.route.item.get import get_item
from auction.route.item.post import post_item
from auction.model.Item import Item
from auction.model.Bid import Bid


async def run():
    await asyncio.sleep(3)
    await Tortoise.init(
        db_url=os.getenv('DB_URL'),
        modules={'models': ['auction.model.Item', 'auction.model.Bid']}
    )
    await Tortoise.generate_schemas()

    app = web.Application()
    app.add_routes([
        web.get('/item/{id}', get_item),
        web.post('/item/{id}/bid', post_bid),
        web.post('/item', post_item)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 9000)
    await site.start()

    print('Server started on 0.0.0.0:9000')

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    run_async(run())
