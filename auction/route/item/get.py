import aiohttp


async def get_item(request):
    id = int(request.match_info.get('id'))
    pool = request.app['connection_pool']

    async with pool.acquire() as connection:
        item_record = await connection.fetchrow('''
            SELECT *
            FROM item
            WHERE item.id = $1
        ''', id)
        bids = await connection.fetch('''
            SELECT *
            FROM bid
            WHERE bid.item_id = $1
        ''', id)

        if not item_record:
            raise aiohttp.web.HTTPNotFound()

        result = dict(item_record)
        result['bids'] = list(map(dict, bids))
        result['auction_end_date'] = item_record['auction_end_date'].timestamp() * \
            1000
        return aiohttp.web.json_response(result)
