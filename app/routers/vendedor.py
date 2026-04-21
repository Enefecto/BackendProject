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
    vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    return vendedor

@router.post("/", response_model=VendedorResponse, status_code=201)
def create_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    email_exists = db.query(Vendedor).filter(Vendedor.email == vendedor.email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    db_vendedor = Vendedor(**vendedor.model_dump())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

@router.patch("/{id}", response_model=VendedorResponse)
def update_vendedor(id: int, vendedor: VendedorUpdate, db: Session = Depends(get_db)):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if not db_vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")

    if vendedor.email:
        email_exists = db.query(Vendedor).filter(Vendedor.email == vendedor.email, Vendedor.id != id).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
            
    for key, value in vendedor.model_dump(exclude_none=True).items():
        setattr(db_vendedor, key, value)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

@router.delete("/{id}", status_code=204)
def delete_vendedor(id: int, db: Session = Depends(get_db)):
    db_vendedor = db.query(Vendedor).filter(Vendedor.id == id).first()
    if not db_vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    db.delete(db_vendedor)
    db.commit()