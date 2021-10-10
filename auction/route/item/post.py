import aiohttp
import datetime
from bson import json_util

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
    client = request.app['mongo']
    auction_end_date = datetime.datetime.utcfromtimestamp(body['auction_end_date'])
    object_id = client.auction.item.insert({"auction_end_date": auction_end_date, 'bids': []})

    return aiohttp.web.Response(
        text=json_util.dumps(object_id),
        content_type='application/json'
    )