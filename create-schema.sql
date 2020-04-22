DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS order_specs;
DROP TABLE IF EXISTS recipe_items;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS ingredients;

CREATE TABLE orders(
    order_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    arrival_date DATE,
    customer_name TEXT,

    PRIMARY KEY (order_id)
);

CREATE TABLE pallets(
    pallet_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    order_id TEXT,
    delivery_id TEXT,
    cookie_name TEXT,
    production_date DATE,
    blocked BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (pallet_id)
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
    FOREIGN KEY (delivery_id) REFERENCES orders(deliveries)
    FOREIGN KEY (cookie_name) REFERENCES orders(cookies)
);

CREATE TABLE deliveries(
    delivery_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    delivery_date DATE,

    PRIMARY KEY (delivery_id)
);

CREATE TABLE order_specs(
    order_id TEXT,
    cookie_name TEXT,
    quantity INT,

    FOREIGN KEY (order_id) REFERENCES orders(order_id)
    FOREIGN KEY (cookie_name) REFERENCES orders(cookies)
);

CREATE TABLE recipe_items(
    cookie_name TEXT,
    ingredient_name TEXT,
    quantity INT,

    FOREIGN KEY (cookie_name) REFERENCES orders(cookies)
    FOREIGN KEY (ingredient_name) REFERENCES orders(ingredients)
);

CREATE TABLE customers(
    customer_name TEXT,
    address TEXT,

    PRIMARY KEY (customer_name)
);

CREATE TABLE cookies(
    cookie_name TEXT,

    PRIMARY KEY (cookie_name)
);

CREATE TABLE ingredients(
    ingredient_name TEXT,
    current_quantity INT,
    unit TEXT,
    delivery_quantity INT,

    PRIMARY KEY (ingredient_name)
);