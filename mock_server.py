# mock_server.py
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/api/auth/login")
def login():
    return {"token": "mock_token"}

@app.get("/api/products")
def get_products():
    return [{"id": 1, "name": "Товар 1"}, {"id": 2, "name": "Товар 2"}]

@app.post("/api/cart/add")
def add_to_cart():
    return {"cart_id": "mock_cart_123"}

@app.post("/api/order/create")
def create_order():
    return JSONResponse(
        content={"status": "заказ создан"},
        status_code=status.HTTP_201_CREATED
    )