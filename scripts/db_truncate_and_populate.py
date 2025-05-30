import sqlite3
import datetime

con = sqlite3.connect("db/dkwity.db")
cur = con.cursor()

# Delete all tables
cur.execute("DELETE FROM clients")
cur.execute("DELETE FROM carts")
cur.execute("DELETE FROM items")
cur.execute("DELETE FROM orders")

cur.execute(f'INSERT INTO "items" ("id","name","price","created_at","updated_at","is_active") \
    VALUES (1, "Item A", 10.0,"{datetime.datetime.now()}","{datetime.datetime.now()}",1), \
        (2, "Item B", 20.0,"{datetime.datetime.now()}","{datetime.datetime.now()}",1), \
        (3, "Item C", 15.0,"{datetime.datetime.now()}","{datetime.datetime.now()}",1), \
        (4, "Item D", 35.0,"{datetime.datetime.now()}","{datetime.datetime.now()}",1)')

cur.execute(f'INSERT INTO "clients" ("id","first_name","last_name","created_at","updated_at","is_active") \
    VALUES (1,"John","Doe","{datetime.datetime.now()}","{datetime.datetime.now()}",1), \
        (2,"Jane","Doe","{datetime.datetime.now()}","{datetime.datetime.now()}",1)')

cur.execute(f'INSERT INTO "carts" ("id","client_id","items","created_at","updated_at","became_order","became_order_at") \
    VALUES (1,1,"[1,2]","{datetime.datetime.now()}","{datetime.datetime.now()}",1,"{datetime.datetime.now()}"), \
        (2,2,"[3,4]","{datetime.datetime.now()}","{datetime.datetime.now()}",1,"{datetime.datetime.now()}"),\
        (3,2,"[1,2,3,4]","{datetime.datetime.now()}","{datetime.datetime.now()}",0,"")')

cur.execute(f'INSERT INTO "orders" ("id","client_id","cart_id","items","created_at","updated_at","is_shipped","shipped_at","total_price","item_qty") \
    VALUES (1,1,1,"[1,2]","{datetime.datetime.now()}","{datetime.datetime.now()}",1,"{datetime.datetime.now()}",30.0,2), \
    (2,2,2,"[3,4]","{datetime.datetime.now()}","{datetime.datetime.now()}",0,"",50.0,2)')


con.commit()
con.close()