from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from typing import List

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"]
)

@router.get("/", response_model=List[ClienteResponse])
def get_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.get("/{id}", response_model=ClienteResponse)
def get_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=ClienteResponse, status_code=201)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.patch("/{id}", response_model=ClienteResponse)
def update_cliente(id: int, cliente: ClienteUpdate, db: Session = Depends(get_db
)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in cliente.model_dump(exclude_none=True).items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{id}", status_code=204)
def delete_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()

