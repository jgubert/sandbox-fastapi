import sqlite3
from .models import Items, Clients, Orders, Carts
import datetime
import ast
import json

def GetItemsNextId(table_name):
    con = sqlite3.connect("db/dkwity.db")
    cur = con.cursor()
    cur.execute(f'select max(id) from {table_name};')
    result = cur.fetchone()
    con.close()

    if result[0] == None:
        return 1
    else:
        return int(result[0]) + 1

def PutRowIntoClass(model, params):
    match model:
        case 'items':
            keys = list(Items.model_fields)
            if len(keys) != len(params):
                return False, {'error': f'{model} - quantidade de campos nao bate.'}
            
            params_dict = {}
            for i in range(len(params)):
                params_dict[keys[i]] = params[i]

            new_model = Items.model_validate(params_dict)

            return True, new_model
        
        case 'clients':
            keys = list(Clients.model_fields)
            if len(keys) != len(params):
                return False, {'error': f'{model} - quantidade de campos nao bate.'}
            
            params_dict = {}
            for i in range(len(params)):
                params_dict[keys[i]] = params[i]

            new_model = Clients.model_validate(params_dict)

            return True, new_model
        
        case 'carts':
            keys = list(Carts.model_fields)
            if len(keys) != len(params):
                return False, {'error': f'{model} - quantidade de campos nao bate.'}
            
            params_dict = {}
            for i in range(len(params)):
                params_dict[keys[i]] = params[i]

            new_model = Carts.model_validate(params_dict)

            return True, new_model
        
        case 'orders':
            keys = list(Orders.model_fields)
            if len(keys) != len(params):
                return False, {'error': f'{model} - quantidade de campos nao bate.'}
            
            params_dict = {}
            for i in range(len(params)):
                params_dict[keys[i]] = params[i]

            new_model = Orders.model_validate(params_dict)

            return True, new_model
        
        case _:
            return False, {'error': 'Modelo nao tratado.'}
        

def GetRowFromDB(table_name: str, id: int):
    try:
        con = sqlite3.connect("db/dkwity.db")
        cur = con.cursor()
        query = f'select * from {table_name} where id = {id};'
        cur.execute(query)
        res = cur.fetchone()
        con.close()

        if res == None:
            return False, {'error': f'{table_name} nao encontrado.'}
        

        exec_success, data_into_model = PutRowIntoClass(table_name, res)
        
        if exec_success:
            return True, data_into_model
        else:
            return False, data_into_model
    
    except Exception as e:
        return False, {'error': e}

def GetAllRowsFromDB(table_name: str):
    try:
        con = sqlite3.connect("db/dkwity.db")
        cur = con.cursor()
        query = f'select * from {table_name};'
        cur.execute(query)
        res = cur.fetchall()
        con.close()

        if res == None:
            return False, {'error': f'{table_name} - nenhum item encontrado.'}
        
        list_item = []
        for row in res:
            #get_item = Items(id=item[0], name=item[1], price=item[2], created_at=item[3], updated_at=item[4], is_active=item[5])
            exec_success, data_into_model = PutRowIntoClass(table_name, row)
            if exec_success:
                list_item.append(data_into_model)
            else:
                return False, data_into_model
            
        return True, list_item
    
    except Exception as e:
        return False, {'error': e}

def DeleteFromTableInDB(table_name: str, id:int):
    try:
        con = sqlite3.connect("db/dkwity.db")
        cur = con.cursor()
        
        # check if record exists
        cur.execute(f'select * from {table_name} where id = {id};')
        res = cur.fetchone()

        if res == None:
            return False, {'error': f'{id} nao encontrado na tabela {table_name}.'}
        
        # delete
        cur.execute(f'delete from {table_name} where id = {id};')
        con.commit()

        # check if not exists anymore
        cur.execute(f'select * from {table_name} where id = {id};')
        res = cur.fetchone()
        con.close()

        if res == None:
            return True, {'message': f'item {id} deletado com sucesso.'}
        
    except Exception as e:
        return False, {'error': e}
    
def UpdateItemOnDB(params: dict):
    # get data from db
    # check which params will be updated
    # prepare and run query
    pass

def WriteItemOnDB(item: Items):
    next_id = GetItemsNextId('items')
    con = sqlite3.connect("db/dkwity.db")
    cur = con.cursor()

    # TODO try
    # Create table clients, to store all the generated keys
    cur.execute(f'INSERT INTO items (id, name, price, created_at, updated_at, is_active) \
        values({next_id}, "{item.name}", {item.price}, "{datetime.datetime.now()}", "{datetime.datetime.now()}", {1});')
    con.commit()
    con.close()

    return True, next_id

def WriteClientOnDB(client: Clients):
    next_id = GetItemsNextId('clients')
    con = sqlite3.connect("db/dkwity.db")
    cur = con.cursor()

    # TODO try
    cur.execute(f'INSERT INTO clients (id, first_name, last_name, created_at, updated_at, is_active) \
        values({next_id}, "{client.first_name}", "{client.last_name}", "{datetime.datetime.now()}", "{datetime.datetime.now()}", {1});')
    
    con.commit()
    con.close()

    return True, next_id
    
def WriteCartOnDB(cart: Carts):
    next_id = GetItemsNextId('carts')
    con = sqlite3.connect("db/dkwity.db")
    cur = con.cursor()

    # TODO try
    cur.execute(f'INSERT INTO carts (id, client_id, items, created_at, updated_at, became_order, became_order_at) \
        values({next_id}, "{cart.client_id}", "{cart.items}", "{datetime.datetime.now()}", "{datetime.datetime.now()}", {0}, "");')
    
    con.commit()
    con.close()

    return True, next_id

def CreateOrderOnDB(order: Orders):
    next_id = GetItemsNextId('orders')
    con = sqlite3.connect("db/dkwity.db")
    con.isolation_level = None
    cur = con.cursor()

    cart_id = order.cart_id
    # check already exists a order for cart_id
    cur.execute(f'select * from orders where cart_id = {cart_id};')
    res = cur.fetchone()

    if res != None:
        return False, {'error': f'ja existe um pedido para o cart_id {cart_id}.'}
    
    # Get data from cart_id
    exec_success, updated_cart = GetRowFromDB('carts', cart_id)
    if not exec_success:
        return False, {'error': 'carrinho nao encontrado.'}
    
    # Get total_price and item_qty from cart
    items = ast.literal_eval(updated_cart.items)
    total_price = 0
    for item in items:
        exec_success, item_data = GetRowFromDB('items', item)
        if not exec_success:
            return False, {'error': 'carrinho {cart_id} - item {item} nao foi encontrado na tabela de items.'}
        total_price = total_price + item_data.price

    item_qty = len(items)
    cur.execute('begin')
    try:
        cur.execute(f'UPDATE carts SET became_order = 1 where id = {cart_id}')
        cur.execute(f'UPDATE carts SET became_order_at = "{datetime.datetime.now()}" where id = {cart_id}')
        cur.execute(f'INSERT INTO orders (id, client_id, cart_id, items, created_at, updated_at, is_shipped, shipped_at, total_price, item_qty) \
            values({next_id}, "{updated_cart.client_id}", {cart_id}, "{updated_cart.items}", "{datetime.datetime.now()}", "{datetime.datetime.now()}", {0}, "", {total_price}, {item_qty})')
        cur.execute(f'COMMIT')
    except con.Error:
        return False, {'error': 'Falha ao criar pedido. Rollback efetuado.'}
    
    con.close()

    return True, next_id

def DeleteOrderOnDB(order_id: int):
    try:
        con = sqlite3.connect("db/dkwity.db")
        cur = con.cursor()
        
        # check if record exists
        cur.execute(f'select * from orders where id = {order_id};')
        res = cur.fetchone()

        if res == None:
            return False, {'error': f'pedido {order_id} nao encontrado na tabela orders.'}
        
        # get cart_id from order
        exec_success, deleted_order = GetRowFromDB('orders', order_id)
        if not exec_success:
            return False, {'error': 'pedido nao encontrado.'}
        
        # delete
        cur.execute('begin')
        try:
            cur.execute(f'delete from orders where id = {order_id};')
            cur.execute(f'UPDATE carts SET became_order = 0 where id = {deleted_order.cart_id}')
            cur.execute(f'UPDATE carts SET became_order_at = "" where id = {deleted_order.cart_id}')
            con.commit()
        except con.Error:
            return False, {'error': 'Falha ao deletar pedido. Rollback efetuado.'}
    
        # check if not exists anymore
        cur.execute(f'select * from orders where id = {order_id};')
        res = cur.fetchone()

        if res == None:
            return True, {'message': f'item {order_id} deletado com sucesso.'}
        
    except Exception as e:
        return False, {'error': e}
    
def SetOrderShipped(order_id: int):
    # test exist order
    # update
    try:
        con = sqlite3.connect("db/dkwity.db")
        cur = con.cursor()
        
        # check if record exists
        cur.execute(f'select * from orders where id = {order_id};')
        res = cur.fetchone()

        if res == None:
            return False, {'error': f'pedido {order_id} nao encontrado na tabela orders.'}

        cur.execute(f'UPDATE orders SET is_shipped = 1 where id = {order_id}')
        cur.execute(f'UPDATE orders SET shipped_at = "{datetime.datetime.now()}" where id = {order_id}')
        con.commit()
        con.close()

        return True, {'message': f'item {order_id} deletado com sucesso.'}
        
    except Exception as e:
        return False, {'error': e}

def GetOrderCompleteInfo(order_id: int):
    # json of all info
    try:
        exec_success, order = GetRowFromDB('orders', order_id)
        if not exec_success:
            return False, {'error': f'pedido {order_id} nao encontrado.'}
        
        exec_success, client = GetRowFromDB('clients', order.client_id)
        if not exec_success:
            return False, {'error': f'pedido {order_id} nao encontrado.'}
        
        items = ast.literal_eval(order.items)
        json_item_list = []
        for item in items:
            exec_success, item_data = GetRowFromDB('items', item)
            if not exec_success:
                return False, {'error': 'carrinho {cart_id} - item {item} nao foi encontrado na tabela de items.'}
            json_item_list.append(json.loads(item_data.model_dump_json()))

        json_order = json.loads(order.model_dump_json())
        json_client = json.loads(client.model_dump_json())


        dict_complete = {
            'id': json_order['id'], 
            'client': json_client, 
            'cart_id': json_order['cart_id'], 
            'items': json_item_list, 
            'created_at': json_order['created_at'], 
            'updated_at': json_order['updated_at'], 
            'is_shipped': json_order['is_shipped'], 
            'shipped_at': json_order['shipped_at'], 
            'total_price': json_order['total_price'],
            'item_qty': json_order['item_qty']
        }
        dict_json = json.dumps(dict_complete)
        json_complete = json.loads(dict_json)
        
        return True, json_complete
    except Exception as e:
        return False, {'error': e}