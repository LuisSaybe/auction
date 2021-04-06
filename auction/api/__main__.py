import os
import asyncio
from aiohttp import web
import asyncpg

from auction.route.bid.post import post_bid
from auction.route.item.get import get_item
from auction.route.item.post import post_item
from auction.utility.db import getConnectionPool


async def main():
    app = web.Application()
    app['connection_pool'] = await getConnectionPool()
    app.add_routes([
        web.get('/item/{id}', get_item),
        web.post('/item/{id}/bid', post_bid),
        web.post('/item', post_item)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 9000)
    await site.start()

    print('API listening on 0.0.0.:9000')

    while True:
        await asyncio.sleep(3600)

app = asyncio.get_event_loop().run_until_complete(main())
