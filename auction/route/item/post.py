import aiohttp

from auction.model.Item import Item
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
    item = Item(auction_end_date=body['auction_end_date'])
    await item.save()
    return aiohttp.web.json_response({'id': item.id})
