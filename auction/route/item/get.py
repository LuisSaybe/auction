import aiohttp
from bson import json_util, ObjectId

async def get_item(request):
    item_id = ObjectId(request.match_info.get('id'))
    client = request.app['mongo']
    item = client.auction.item.find_one({"_id": item_id})

    if not item:
        raise aiohttp.web.HTTPNotFound()

    return aiohttp.web.Response(
        text=json_util.dumps(item),
        content_type='application/json'
    )