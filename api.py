from bottle import get, post, run, request, response
from datetime import date
import sqlite3
import json

conn = sqlite3.connect("krusty-db.sqlite", check_same_thread=False)


def format_response(d):
    return json.dumps(d, indent=4) + "\n"

#curl -X POST http://localhost:8888/reset
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
    return format_response({"status": "ok"})

#curl -X GET http://localhost:8888/customers
@get('/customers')
def get_customers():
    c = conn.cursor()
    c.execute(
    """
    SELECT *
    FROM customers
    WHERE 1=1
    """
    )
    data = [{'name': customer_name, 'address': address}
            for (customer_name, address) in c]
    return format_response({"customers": data})        

#curl -X GET http://localhost:8888/ingredients
@get('/ingredients')
def get_ingredients():
    c = conn.cursor()
    c.execute(
    """
    SELECT ingredient_name, current_quantity, unit
    FROM ingredients
    WHERE 1=1
    """
    )
    data = [{'name': ingredient_name, 'quantity': current_quantity, 'unit': unit}
    for (ingredient_name, current_quantity, unit) in c]
    return format_response({"ingredients": data})

#curl -X GET http://localhost:8888/cookies
@get('/cookies')
def get_cookies():
    c = conn.cursor()
    c.execute(
    """
    SELECT cookie_name
    FROM cookies
    ORDER BY cookie_name ASC
    """
    )
    data = [{'name': cookie_name[0]} for (cookie_name) in c]
    return format_response({"cookies": data})

#curl -X GET http://localhost:8888/recipes
@get('/recipes')
def get_recipes():
    c = conn.cursor()
    c.execute(
    """
    SELECT cookie_name, ingredient_name, quantity, unit
    FROM recipe_items
    JOIN ingredients
    USING (ingredient_name)
    WHERE 1=1
    ORDER BY cookie_name, ingredient_name ASC
    """
    )
    data = [{'cookie': cookie_name, 'ingredient': ingredient_name, 'quantity': quantity, 'unit': unit}
    for (cookie_name, ingredient_name, quantity, unit) in c]
    return format_response({"recipes": data})

#curl -X POST http://localhost:8888/pallets\?cookie\=Berliner
@post('/pallets')
def add_pallet():
    cookie = request.query.cookie
    c = conn.cursor()
    c.executescript(
      """
      DROP TRIGGER IF EXISTS cookie_checker;
      CREATE TRIGGER cookie_checker
      BEFORE INSERT ON pallets
      WHEN NEW.cookie_name NOT IN (SELECT cookie_name FROM cookies)
      BEGIN
        SELECT RAISE(ROLLBACK, 'No such cookie');
      END;
 
      DROP TRIGGER IF EXISTS pantry_checker;
      CREATE TRIGGER pantry_checker
      BEFORE UPDATE ON ingredients
      WHEN NEW.current_quantity < 0 
      BEGIN
        SELECT RAISE(ROLLBACK, 'not enough ingredients');
      END;
      """
    )
    conn.commit()
    try:
      c.execute(
          """
          INSERT OR REPLACE
          INTO pallets(cookie_name, production_date)
          VALUES (?, ?)
          """, [cookie, str(date.today())]
      )
    except Exception:
      response.status = 500
      return format_response({'status': 'no such cookie'})
    try:
      c.execute(
          """
          UPDATE ingredients
          SET current_quantity = current_quantity - (SELECT quantity FROM recipe_items WHERE cookie_name = ? 
                                                     AND recipe_items.ingredient_name = ingredients.ingredient_name) * 54
          WHERE ingredient_name IN (SELECT ingredient_name FROM recipe_items WHERE cookie_name = ?)
          """, [cookie,cookie]
      )
    except Exception:
      response.status = 500
      return format_response({'status': 'not enough ingredients'})
    conn.commit()
    c.execute(
          """
          SELECT pallet_id AS id
          FROM pallets
          WHERE rowid = last_insert_rowid()
          """
    )
    response.status = 200
    return json.dumps({'status' : 'ok', 'id' : c.fetchone()[0]}, indent=4) + "\n"

#curl -X GET http://localhost:8888/pallets
@get('/pallets')
def get_pallets():
    query = """
        SELECT pallet_id, cookie_name, production_date, customer_name, blocked
        FROM pallets
        LEFT JOIN orders
        USING (order_id)
        LEFT JOIN customers
        USING (customer_name)
        WHERE 1=1
        """
    
    params = []

    if request.query.cookie:
    	query += "AND cookie_name = ?"
    	params.append(request.query.cookie)
    if request.query.blocked:
    	query += "AND blocked = ?"
    	params.append(request.query.blocked)
    if request.query.before:
    	query += "AND production_date < ?"
    	params.append(request.query.before)
    if request.query.after:
    	query += "AND production_date > ?"
    	params.append(request.query.after)

    c = conn.cursor()
    c.execute(
    	query,
    	params
    )

    data =[{'id':pallet_id, 'cookie': cookie_name, 'productionDate': production_date, 'customer': customer_name, 'blocked': blocked}
    for (pallet_id, cookie_name, production_date, customer_name, blocked) in c]
    return format_response({"pallets": data})

#curl -X POST http://localhost:8888/block/<cookie-name>/<from-date>/<to-date>
@post('/block/<cookie_name>/<from_date>/<to_date>')
def add_block(cookie_name, from_date, to_date):
    c = conn.cursor()
    c.execute(
        """
        UPDATE pallets
        SET blocked = 1
        WHERE cookie_name = ? AND production_date BETWEEN ? AND ?
        """, [cookie_name, from_date, to_date]
    )

    conn.commit()
    return format_response({"status": "ok"})

#curl -X POST http://localhost:8888/unblock/<cookie-name>/<from-date>/<to-date>
@post('/unblock/<cookie_name>/<from_date>/<to_date>')
def add_unblock(cookie_name, from_date, to_date):
    c = conn.cursor()
    c.execute(
        """
        UPDATE pallets
        SET blocked = 0
        WHERE cookie_name = ? AND production_date BETWEEN ? AND ?
        """, [cookie_name, from_date, to_date]
    )

    conn.commit()
    return format_response({"status": "ok"})

run(host='localhost', port=8888)