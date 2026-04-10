from fastapi import FastAPI
from app.routers import producto, cliente
from app.db import Base, engine
from app.models import producto as producto_model, cliente as cliente_model

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(producto.router)
app.include_router(cliente.router)

@app.get("/")
def root():
    return {"message": "Hola mundo"}