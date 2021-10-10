import aiohttp
import time
from bson import ObjectId

from auction.utility.validate import validate_schema

@validate_schema({
    "type": "object",
    "properties": {
        "amount": {"type": "number", "exclusiveMinimum": 0},
        "user_id": {"type": "string"},
    },
    "required": ["amount", "user_id"]
})
async def post_bid(request):
    item_id = ObjectId(request.match_info.get('id'))
    body = await request.json()
    client = request.app['mongo']
    item = client.auction.item.find_one({"_id": item_id})

    if not item:
        raise aiohttp.web.HTTPNotFound()

    if item['auction_end_date'].timestamp() < time.time():
        raise aiohttp.web.HTTPBadRequest(text=f'Auction has expired')

    sorted_bids = sorted(item['bids'], key=lambda item: item['amount'])

    if len(sorted_bids) > 0 and sorted_bids[-1]['amount'] >= body['amount']:
        raise aiohttp.web.HTTPBadRequest(text=f"bid amount must be greater than {sorted_bids[-1]['amount']}")

    next_bid = { 'user_id': ObjectId(body['user_id']), 'amount': body['amount'] }

    client.auction.item.update_one(
        {"_id" : item_id},
        {
            "$push": {"bids": next_bid}
        }
    )

    return aiohttp.web.Response()
