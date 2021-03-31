import aiohttp

from auction.utility.validate import validate_schema
from tortoise.contrib.pydantic import pydantic_model_creator

from auction.model.Bid import Bid
from auction.model.Item import Item


@validate_schema({
    "type": "object",
    "properties": {
        "amount": {"type": "number", "exclusiveMinimum": 0},
        "user_id": {"type": "number"},
    },
    "required": ["amount", "user_id"]
})
async def post_bid(request):
    item_id = int(request.match_info.get('id'))
    searched_items = await Item.filter(id=item_id)

    if len(searched_items) == 0:
        raise aiohttp.web.HTTPNotFound()

    body = await request.json()
    items_with_greater_bid = await Bid.filter(item__id=item_id, amount__gte=body['amount']).count()

    if items_with_greater_bid > 0:
        raise aiohttp.web.HTTPBadRequest(text='bid amount too low')

    bid = Bid(amount=body['amount'], item_id=item_id, user_id=body['user_id'])
    await bid.save()
    return aiohttp.web.Response()
