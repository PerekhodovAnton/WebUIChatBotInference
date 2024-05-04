CREATE TABLE users (
    userid SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255)
);

CREATE TABLE queries (
    queryid BIGSERIAL PRIMARY KEY,
    message VARCHAR(255),
    validity VARCHAR(255),
    date_time TIMESTAMP,
    userid INTEGER REFERENCES users(userid)
);

CREATE TABLE responses (
    responseid BIGSERIAL PRIMARY KEY,
    text VARCHAR(255),
    date_time TIMESTAMP,
    queryid INTEGER REFERENCES queries(queryid)
);
