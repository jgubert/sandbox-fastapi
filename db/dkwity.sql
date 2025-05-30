BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "carts" (
	"id"	integer,
	"client_id"	integer,
	"items"	text,
	"created_at"	text,
	"updated_at"	text,
	"became_order"	integer,
	"became_order_at"	text,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clients" (
	"id"	integer,
	"first_name"	text,
	"last_name"	text,
	"created_at"	text,
	"updated_at"	text,
	"is_active"	integer,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "items" (
	"id"	integer,
	"name"	text,
	"price"	float,
	"created_at"	text,
	"updated_at"	text,
	"is_active"	integer,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "orders" (
	"id"	integer,
	"client_id"	integer,
	"cart_id"	integer,
	"items"	text,
	"created_at"	text,
	"updated_at"	text,
	"is_shipped"	integer,
	"shipped_at"	text,
	"total_price"	float,
	"item_qty"	integer,
	PRIMARY KEY("id")
);
INSERT INTO "carts" ("id","client_id","items","created_at","updated_at","became_order","became_order_at") VALUES (1,1,'[1,2]','2025-05-28 13:39:41.579614','2025-05-28 13:39:41.579626',1,'2025-05-28 16:56:27.923722'),
 (2,2,'[3]','2025-05-28 13:40:14.805949','2025-05-28 13:40:14.805969',0,'');
INSERT INTO "clients" ("id","first_name","last_name","created_at","updated_at","is_active") VALUES (1,'john','doe','2025-05-28 01:44:04.113150','2025-05-28 01:44:04.113167',1),
 (2,'jane','doe','2025-05-28 01:44:14.674159','2025-05-28 01:44:14.674182',1);
INSERT INTO "items" ("id","name","price","created_at","updated_at","is_active") VALUES (1,'frango',17.0,'2025-05-25 12:59:21.051601','2025-05-25 12:59:21.051654',1),
 (2,'cartolina',20.0,'2025-05-25 13:09:55.013906','2025-05-25 13:09:55.013930',1),
 (3,'papel-cartao',10.0,'2025-05-25 13:10:36.211144','2025-05-25 13:10:36.211161',1),
 (4,'sulfite-75',20.0,'2025-05-25 13:11:04.498658','2025-05-25 13:11:04.498681',1);
INSERT INTO "orders" ("id","client_id","cart_id","items","created_at","updated_at","is_shipped","shipped_at","total_price","item_qty") VALUES (1,1,1,'[1,2]','2025-05-28 16:56:27.923799','2025-05-28 16:56:27.923806',1,'2025-05-28 16:58:48.229860',0.0,0);
COMMIT;
