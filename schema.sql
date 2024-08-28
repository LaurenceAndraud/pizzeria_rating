CREATE TABLE if not exists users (
    id PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) UNIQUE NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists pizzerias (
    id PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists rate (
    id PRIMARY KEY,
    users_id INTEGER REFERENCES users(id),
    pizzerias_id INTEGER REFERENCES pizzerias(id),
    rate INTEGER CHECK (note >=0 AND note <= 5),
    comment TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);