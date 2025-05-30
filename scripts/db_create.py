import sqlite3

con = sqlite3.connect("db/dkwity.db")
cur = con.cursor()

# TODO create table clients_keys, to store all the generated keys

# Create table clients
cur.execute("CREATE TABLE IF NOT EXISTS clients(" \
    "id integer primary key, " \
    "first_name text, " \
    "last_name text, " \
    "created_at text, " \
    "updated_at text, " \
    "is_active integer)"
)

# Create table carts
cur.execute("CREATE TABLE IF NOT EXISTS carts(" \
    "id integer primary key, " \
    "client_id integer, " \
    "items text, " \
    "created_at text, " \
    "updated_at text, " \
    "became_order integer," \
    "became_order_at text)"
)

# Create table orders
cur.execute("CREATE TABLE IF NOT EXISTS orders(" \
    "id integer primary key, " \
    "client_id integer, " \
    "cart_id integer, " \
    "items text, " \
    "created_at text, " \
    "updated_at text, " \
    "is_shipped integer," \
    "shipped_at text," \
    "total_price float," \
    "item_qty integer)"
)

# Create table items
cur.execute("CREATE TABLE IF NOT EXISTS items(" \
    "id integer primary key, " \
    "name text, " \
    "price float, " \
    "created_at text, " \
    "updated_at text, " \
    "is_active integer)"
)