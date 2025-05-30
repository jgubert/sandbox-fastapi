from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .models import Items, Clients, Carts, Orders
from .utils import WriteItemOnDB, DeleteFromTableInDB, UpdateItemOnDB, \
    WriteClientOnDB, GetRowFromDB, WriteCartOnDB, GetAllRowsFromDB,  \
    CreateOrderOnDB, DeleteOrderOnDB, SetOrderShipped, GetOrderCompleteInfo

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# CRUD Items
@app.post('/create-item/')
def create_item(temp_item: Items):
    new_item = Items(name=temp_item.name, price=temp_item.price)

    write_result, item_id = WriteItemOnDB(new_item)
        
    return JSONResponse(status_code=200, content=str({'message': f'item {item_id} criado com sucesso!'}))

@app.get('/get-item/{item_id}')
def get_item(item_id: int):
    exec_success, res = GetRowFromDB('items', item_id)

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))

# listar todos os items
@app.get('/list-items')
def list_all_items():
    exec_success, res = GetAllRowsFromDB('items')

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))

# deletar um item
@app.delete('/delete-item/{item_id}')
def delete_item(item_id: int):
    exec_success, res = DeleteFromTableInDB('items', item_id)

    if exec_success:
        return JSONResponse(status_code=200, content=str(res))
    else:
        return JSONResponse(status_code=500, content=str(res))
    
# update de um item
#@app.put('update-item/{item_id}')
#def update_item(item_id: int, name: str = None, price: float = None, is_active: str = None):
#    # put params <> None in a dict
#    pass

# CRUD Clients
@app.post('/create-client/')
def create_client(temp_client: Clients):
    new_client = Clients(first_name=temp_client.first_name, last_name=temp_client.last_name)

    write_result, client_id = WriteClientOnDB(new_client)
        
    return JSONResponse(status_code=200, content=str({'message': f'cliente {client_id} criado com sucesso!'}))

@app.get('/get-client/{client_id}')
def get_client(client_id: int):
    exec_success, res = GetRowFromDB('clients', client_id)

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))

@app.get('/list-clients')
def list_all_clients():
    exec_success, res = GetAllRowsFromDB('clients')

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))
    
@app.delete('/delete-client/{client_id}')
def delete_client(client_id: int):
    exec_success, res = DeleteFromTableInDB('clients', client_id)

    if exec_success:
        return JSONResponse(status_code=200, content=str(res))
    else:
        return JSONResponse(status_code=500, content=str(res))

# CRUD Carts
@app.post('/create-cart/')
def create_cart(temp_cart: Carts):
    new_cart = Carts(client_id=temp_cart.client_id, items=temp_cart.items)

    write_result, cart_id = WriteCartOnDB(new_cart)
        
    return JSONResponse(status_code=200, content=str({'message': f'carrinho {cart_id} criado com sucesso!'}))

@app.get('/get-cart/{cart_id}')
def get_cart(cart_id: int):
    exec_success, res = GetRowFromDB('carts', cart_id)

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))

@app.get('/list-carts')
def list_all_carts():
    exec_success, res = GetAllRowsFromDB('carts')

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))
    
@app.delete('/delete-cart/{cart_id}')
def delete_cart(cart_id: int):
    exec_success, res = DeleteFromTableInDB('carts', cart_id)

    if exec_success:
        return JSONResponse(status_code=200, content=str(res))
    else:
        return JSONResponse(status_code=500, content=str(res))
    
# CRUD Orders
@app.post('/create-order/')
def create_order(temp_order: Orders):
    new_order = Orders(cart_id=temp_order.cart_id)

    write_result, order_id = CreateOrderOnDB(new_order)
        
    if write_result:
        return JSONResponse(status_code=200, content=str({'message': f'pedido {order_id} criado com sucesso!'}))
    else:
        return JSONResponse(status_code=500, content=str(order_id))

@app.get('/get-order/{order_id}')
def get_order(order_id: int):
    exec_success, res = GetRowFromDB('orders', order_id)

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))

@app.get('/list-orders')
def list_all_orders():
    exec_success, res = GetAllRowsFromDB('orders')

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))

@app.delete('/delete-order/{order_id}')
def delete_order(order_id: int):
    exec_success, res = DeleteOrderOnDB(order_id)

    if exec_success:
        return JSONResponse(status_code=200, content=str(res))
    else:
        return JSONResponse(status_code=500, content=str(res))
    
@app.post('/order-shipped')
def order_shipped(order_id: int):
    exec_success, res = SetOrderShipped(order_id)

    if exec_success:
        return JSONResponse(status_code=200, content=str(res))
    else:
        return JSONResponse(status_code=500, content=str(res))
    
@app.get('/get-order-complete-info/{order_id}')
def order_get_complete_info(order_id: int):
    exec_success, res = GetOrderCompleteInfo(order_id)

    if exec_success:
        json_item = jsonable_encoder(res)
        return JSONResponse(status_code=200, content=json_item)
    else:
        return JSONResponse(status_code=500, content=str(res))