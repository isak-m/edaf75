from bottle import get, post, run, request, response
import sqlite3
import json

conn = sqlite3.connect("krusty-db.sqlite", check_same_thread=False)


def format_response(d):
    return json.dumps(d, indent=4) + "\n"

@post('/reset')
def reset_tables():
    c = conn.cursor()
    c.executescript(
    """
    DELETE
    FROM orders;

    DELETE
    FROM pallets;

    DELETE
    FROM deliveries;

    DELETE
    FROM order_specs;

    DELETE
    FROM recipe_items;

    DELETE
    FROM customers;

    DELETE
    FROM cookies;

    DELETE
    FROM ingredients;

    INSERT OR REPLACE
    INTO customers(customer_name, address)
    VALUES ("Finkakor AB", "Helsingborg"),
           ("Småbröd AB", "Malmö"),
           ("Kaffebröd AB", "Landskrona"),
           ("Bjudkakor AB", "Ystad"),
           ("Kalaskakor AB", "Trelleborg"),
           ("Partykakor AB", "Kristianstad"),
           ("Gästkakor AB", "Hässleholm"),
           ("Skånekakor AB", "Perstorp");

    INSERT OR REPLACE
    INTO cookies(cookie_name)
    VALUES ("Nut ring"),
           ("Nut cookie"),
           ("Amneris"),
           ("Tango"),
           ("Almond delight"),
           ("Berliner");

    INSERT OR REPLACE
    INTO ingredients(ingredient_name, current_quantity, unit)
    VALUES ("Flour", 100000, "g"),
           ("Butter", 100000, "g"),
           ("Icing sugar", 100000, "g"),
           ("Roasted, chopped nuts", 100000, "g"),
           ("Fine-ground nuts", 100000, "g"),
           ("Ground, roasted nuts", 100000, "g"),
           ("Bread crumbs", 100000, "g"),
           ("Sugar", 100000, "g"),
           ("Egg whites", 100000, "ml"),
           ("Chocolate", 100000, "g"),
           ("Marzipan", 100000, "g"),
           ("Eggs", 100000, "g"),
           ("Potato starch", 100000, "g"),
           ("Wheat flour", 100000, "g"),
           ("Sodium bicarbonate", 100000, "g"),
           ("Vanilla", 100000, "g"),
           ("Chopped almonds", 100000, "g"),
           ("Cinnamon", 100000, "g"),
           ("Vanilla sugar", 100000, "g");
    
    INSERT OR REPLACE
    INTO recipe_items(cookie_name, ingredient_name, quantity)
    VALUES ("Nut ring", "Flour", 450),
           ("Nut ring", "Butter", 450),
           ("Nut ring", "Icing sugar", 190),
           ("Nut ring", "Roasted, chopped nuts", 225),
           ("Nut cookie", "Fine-ground nuts", 750),
           ("Nut cookie", "Ground, roasted nuts", 625),
           ("Nut cookie", "Bread crumbs", 125),
           ("Nut cookie", "Sugar", 375),
           ("Nut cookie", "Egg whites", 350),
           ("Nut cookie", "Chocolate", 50),
           ("Amneris", "Marzipan", 750),
           ("Amneris", "Butter", 250),
           ("Amneris", "Eggs", 250),
           ("Amneris", "Potato starch", 25),
           ("Amneris", "Wheat flour", 25),
           ("Tango", "Butter", 200),
           ("Tango", "Sugar", 250),
           ("Tango", "Flour", 300),
           ("Tango", "Sodium bicarbonate", 4),
           ("Tango", "Vanilla", 2),
           ("Almond delight", "Butter", 400),
           ("Almond delight", "Sugar", 270),
           ("Almond delight", "Chopped almonds", 279),
           ("Almond delight", "Flour", 400),
           ("Almond delight", "Cinnamon", 10),
           ("Berliner", "Flour", 350),
           ("Berliner", "Butter", 250),
           ("Berliner", "Icing sugar", 100),
           ("Berliner", "Eggs", 50),
           ("Berliner", "Vanilla sugar", 5),
           ("Berliner", "Chocolate", 50);
     """
    )
    conn.commit()
    response.status = 200
    return format_response({'Status': response.status})

run(host='localhost', port=8888)