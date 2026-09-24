CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    address VARCHAR,
    is_open BOOLEAN NOT NULL DEFAULT TRUE,
    opening_hours VARCHAR,
    contact VARCHAR
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL CHECK (role IN ('admin', 'staff', 'direction')),
    restaurant_id INTEGER REFERENCES restaurants(id)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    image VARCHAR,
    description VARCHAR,
    category VARCHAR,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
    ingredients TEXT[] NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS orders (
    order_number SERIAL PRIMARY KEY,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    total_price NUMERIC(10, 2) NOT NULL CHECK (total_price > 0),
    status VARCHAR NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'validated', 'preparing', 'ready', 'collected', 'cancelled')),
    pickup_mode VARCHAR NOT NULL CHECK (pickup_mode IN ('onsite', 'takeaway')),
    customer_name VARCHAR NOT NULL,
    customer_email VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_number),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL
);