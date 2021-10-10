import aiohttp
from bson import json_util

def list_items(request):
    skip = int(request.query['skip'])
    client = request.app['mongo']

    cursor = client.auction.item.find(
        {},
        projection=None,
        skip=skip,
        limit=100
    )
    items = list(cursor)

    return aiohttp.web.Response(
        text=json_util.dumps(items),
        content_type='application/json'
    )