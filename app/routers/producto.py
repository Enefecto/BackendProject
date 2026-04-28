from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.producto import Producto
from app.models.vendedor import Vendedor
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from typing import List
from app.utils.helpers import get_or_404

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

@router.get("/", response_model=List[ProductoResponse])
def get_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.get("/{id}", response_model=ProductoResponse)
def get_producto(id: int, db: Session = Depends(get_db)):

    # Verificar y retornar si existe el Producto
    return get_or_404(db, Producto, id, "Producto no encontrado")

@router.post("/", response_model=ProductoResponse, status_code=201)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    
    # Verificar si el vendedor existe mediante su ID
    vendedor_existe = db.query(Vendedor).filter(Vendedor.id == producto.id_vendedor).first()
    if not vendedor_existe:
        raise HTTPException(status_code=404, detail="El ID del vendedor no existe")
    
    # Crear Producto
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.patch("/{id}", response_model=ProductoResponse)
def update_producto(id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):

    # Verificar que el producto exista
    db_producto = get_or_404(db, Producto, id, "Producto no encontrado")

    # Verificar si el vendedor existe mediante su ID, solo si lo actualizarán
    if producto.id_vendedor is not None:
        vendedor_existe = db.query(Vendedor).filter(Vendedor.id == producto.id_vendedor).first()
        if not vendedor_existe:
            raise HTTPException(status_code=404, detail="El ID del vendedor no existe")

    # Actualizar producto
    for key, value in producto.model_dump(exclude_none=True).items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

from sqlalchemy.exc import IntegrityError

@router.delete("/{id}", status_code=204)
def delete_producto(id: int, db: Session = Depends(get_db)):
    db_producto = get_or_404(db, Producto, id, "Producto no encontrado")
    try:
        db.delete(db_producto)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un producto que tiene pedidos asociados"
        )