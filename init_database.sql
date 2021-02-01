CREATE TABLE listings (
    item_id BIGINT,
    max_bid INT,
    name VARCHAR(512),
    ending_dt TIMESTAMP
);

CREATE TABLE process (
    pid BIGINT
);