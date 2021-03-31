from aiohttp import web


async def post_bid(request):
    name = request.match_info.get('id')
    return web.Response(text=name)
