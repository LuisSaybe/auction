import aiohttp
from tortoise.contrib.pydantic import pydantic_model_creator
from auction.model.Item import Item


async def get_item(request):
    id = request.match_info.get('id')
    searched_item = await Item.get(id=id)

    if not searched_item:
        raise aiohttp.web.HTTPNotFound()

    item_pydantic = pydantic_model_creator(Item)
    p = await item_pydantic.from_tortoise_orm(searched_item)
    return aiohttp.web.Response(body=p.json(), headers={'Content-Type': 'application/json'})
