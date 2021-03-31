from aiohttp import web
from auction.model.Item import Item


async def get_item(request):
    id = request.match_info.get('id')
    item = await Item.filter(id=id)
    return web.Response(text=str(item.id))
