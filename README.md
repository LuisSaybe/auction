# An Auctioning System

This project aims to create a simple auctioning system deployable to [Digital Ocean's Kubernetes](https://www.digitalocean.com/products/kubernetes) backed by [postgresql](https://www.postgresql.org) and [aiohttp](https://github.com/aio-libs/aiohttp)

## HTTP Endpoints

### POST /item

**Example Body**

- **auction_end_date** the number of seconds since the unix epoch. This field is immutable

```json
{ "auction_end_date": 1619981760 }
```

**Example Response**

- the id of the created item

```
6
```

### POST /item/{id}/bid

**Example Body**

- **amount** bid amount as integer
- **user_id** the positive integer id of the bidding user

- a bid can not be placed if it is equal to or less than any other existing bid for an item
- a bid can not be placed after `auction_end_date`

```json
{ "amount": 43, "user_id": 2 }
```

### GET /item/{id}

- **highest_bidder** the certified highest bidder determined after `auction_end_date` by a backend cronjob
- **bids** an array of bids for this item

**Example Response**

```json
{
  "id": 6,
  "auction_end_date": 1619981640.0,
  "highest_bidder": null,
  "bids": [
    {
      "id": 1,
      "amount": 43,
      "item_id": 6,
      "user_id": 2
    }
  ]
}
```

### Determining the Highest Bidder

When the `auction_end_date` is in the past and its `highest_bidder` is `null`, an item will become eligible to be processed by the cron job defined in the python module `auction/cron/certify_item`. This cron job runs every 2 minutes and writes to the `highest_bidder` field for each item. If no `highest_bidder` can be found, `-1` is written to this field.

It is not needed to run a cron job to write to `highest_bidder` since each succesful write to call to `POST /item/{id}/bid` can determine the highest_bidder, even without the need for the database field `item.highest_bidder`. This project also aims to also show how `kind: CronJob` can be used in `kubernetes` and represent other additional transactions which can be run after an auction has ended. A messaging queue can also be used to represent these steps.
