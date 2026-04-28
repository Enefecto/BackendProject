from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorResponse
from typing import List

router = APIRouter(
    prefix="/vendedores",
    tags=["vendedores"]
)

@router.get("/", response_model=List[VendedorResponse])
def get_vendedores(db: Session = Depends(get_db)):
    return db.query(Vendedor).all()

@router.get("/{id}", response_model=VendedorResponse)
def get_vendedor(id: int, db: Session = Depends(get_db)):
    # Verificar que el Vendedor exista
    vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    
    # Retornar Vendedor
    return vendedor

@router.post("/", response_model=VendedorResponse, status_code=201)
def create_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):

    # Verificar que el email no exista
    email_existe = db.query(Vendedor).filter(Vendedor.email == vendedor.email).first()
    if email_existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Verificar que el telefono no exista, solo si se envia al crear
    if vendedor.telefono is not None:
        telefono_existe = db.query(Vendedor).filter(Vendedor.telefono == vendedor.telefono).first()
        if telefono_existe:
            raise HTTPException(status_code=400, detail="El telefono ya esta registrado")

    # Crear Vendedor
    db_vendedor = Vendedor(**vendedor.model_dump())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

@router.patch("/{id}", response_model=VendedorResponse)
def update_vendedor(id: int, vendedor: VendedorUpdate, db: Session = Depends(get_db)):

    # Verificar que el id del Vendedor exista
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if not db_vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")

    # Verificar que el email no existe en otros Vendedores ignorando el del propetario
    if vendedor.email:
        email_existe = db.query(Vendedor).filter(Vendedor.email == vendedor.email, Vendedor.id != id).first()
        if email_existe:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar que el telefono no existe en otros Vendedores ignorando el del propetario
    if vendedor.telefono:
        telefono_existe = db.query(Vendedor).filter(Vendedor.telefono == vendedor.telefono, Vendedor.id != id). first()
        if telefono_existe:
            raise HTTPException(status_code=400, detail="El telefono ya está registrado")

    # Actualizar Vendedor
    for key, value in vendedor.model_dump(exclude_none=True).items():
        setattr(db_vendedor, key, value)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

@router.delete("/{id}", status_code=204)
def delete_vendedor(id: int, db: Session = Depends(get_db)):

    # Verificar que el Vendedor exista antes de eliminar
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if not db_vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    
    # Eliminar
    db.delete(db_vendedor)
    db.commit()