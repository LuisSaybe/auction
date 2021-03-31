import datetime

from aiohttp import web
from auction.model.Item import Item


async def post_item(request):
    body = await request.json()
    item = Item(auction_end_date=datetime.datetime.now())
    await item.save()
    return web.Response(text=str(item.id))
