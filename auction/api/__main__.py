import os
import asyncio
from aiohttp import web
from pymongo import MongoClient

from auction.route.bid.post import post_bid
from auction.route.item.get import get_item
from auction.route.item.list import list_items
from auction.route.item.post import post_item

async def main():
    app = web.Application()
    app['mongo'] = MongoClient(os.environ['DB_URL'])
    app.add_routes([
        web.get('/item/{id}', get_item),
        web.post('/item/{id}/bid', post_bid),
        web.post('/item', post_item),
        web.get('/item', list_items)
    ])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 9000)
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
