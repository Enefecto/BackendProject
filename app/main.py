from fastapi import FastAPI
from app.routers import producto
from app.db import Base, engine
from app.models import producto as producto_model

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(producto.router)

@app.get("/")
def root():
    return {"message": "Hola mundo"}