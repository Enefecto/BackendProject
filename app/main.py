from fastapi import FastAPI
from app.routers import producto, cliente, vendedor, pedido

app = FastAPI()

app.include_router(producto.router)
app.include_router(cliente.router)
app.include_router(vendedor.router)
app.include_router(pedido.router)

@app.get("/")
def root():
    return {"message": "Hola mundo"}