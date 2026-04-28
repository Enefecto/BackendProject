from fastapi import FastAPI
from app.routers import producto, cliente, vendedor, pedido
from app.db import Base, engine
from app.models import producto as producto_model, cliente as cliente_model, vendedor as vendedor_model, pedido as pedido_model, pedido_producto as pedido_producto_model

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(producto.router)
app.include_router(cliente.router)
app.include_router(vendedor.router)
app.include_router(pedido.router)

@app.get("/")
def root():
    return {"message": "Hola mundo"}