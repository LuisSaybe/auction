# An Auctioning System

This project aims to create an auctioning system deployable to [EKS](https://aws.amazon.com/eks/) on AWS backed by [mongo](https://www.mongodb.com/) and [aiohttp](https://github.com/aio-libs/aiohttp)

## HTTP Endpoints

### POST /item

**Example Body**

- **auction_end_date** the number of seconds since the unix epoch. This field is immutable

```json
{ "auction_end_date": 1619981760 }
```

**Example Response**

- the id of the created item

```json
{
  "$oid": "61622c8ed1a52eba00ea05dd"
}
```

### POST /item/{id}/bid

**Example Body**

- **amount** bid amount as integer
- **user_id** the id of the bidding user

- a bid can not be placed if it is equal to or less than any other existing bid for an item
- a bid can not be placed after `auction_end_date`

```json
{ "amount": 43, "user_id": "6162257cbe78eb43c6e95d4b" }
```

### GET /item/{id}

- **highest_bidder** the certified highest bidder determined after `auction_end_date` by a backend cronjob
- **bids** an array of bids for this item

**Example Response**

```json
{
  "_id": {
    "$oid": "6162257cbe78eb43c6e95d4b"
  },
  "auction_end_date": {
    "$date": 233800913000
  },
  "bids": []
}
```
