CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    auction_end_date TIMESTAMP NOT NULL
);

CREATE TABLE bid (
    id SERIAL PRIMARY KEY,
    amount INT NOT NULL,
    item_id INT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_bid_item FOREIGN KEY(item_id) REFERENCES item(id)
);