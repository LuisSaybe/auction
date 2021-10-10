import os
import asyncio
from datetime import datetime

from pymongo import MongoClient

def main():
    client = MongoClient(os.environ['DB_URL'])
    search = {
        "auction_end_date": { "$lt": datetime.now() },
        "sold_to": { "$exists": False }
    }
    item = client.auction.item.find_one(search)

    while item:
        bids = sorted(item['bids'], key=lambda item: item['amount'])
        highest_bid = bids[-1]if len(bids) > 0 else None
        client.auction.item.update_one(
            {"_id" : item['_id']},
            {
                "$set": {'sold_to': highest_bid['user_id'] }
            }
        )

        item = client.auction.item.find_one(search)


if __name__ == '__main__':
    main()