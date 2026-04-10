from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from typing import List

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

@router.get("/", response_model=List[ProductoResponse])
def get_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.get("/{id}", response_model=ProductoResponse)
def get_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoResponse, status_code=201)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.patch("/{id}", response_model=ProductoResponse)
def update_producto(id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.model_dump(exclude_none=True).items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{id}", status_code=204)
def delete_producto(id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()