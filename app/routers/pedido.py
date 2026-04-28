from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.pedido import Pedido
from app.models.pedido_producto import PedidoProducto
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoResponse
from app.utils.helpers import get_or_404
from typing import List

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"]
)

@router.get("/", response_model=List[PedidoResponse])
def get_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

@router.get("/{id}", response_model=PedidoResponse)
def get_pedido(id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Pedido, id, "Pedido no encontrado")

@router.post("/", response_model=PedidoResponse, status_code=201)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):

    # Verificar que el cliente existe si se manda
    if pedido.id_cliente is not None:
        get_or_404(db, Cliente, pedido.id_cliente, "Cliente no encontrado")

    # Crear el pedido
    db_pedido = Pedido(id_cliente=pedido.id_cliente)
    db.add(db_pedido)
    db.flush()  # genera el id sin hacer commit

    # Agregar productos al pedido
    total = 0.0
    for item in pedido.productos:
        db_producto = get_or_404(db, Producto, item.id_producto, "Producto no encontrado")

        db_item = PedidoProducto(
            id_pedido=db_pedido.id,
            id_producto=item.id_producto,
            cantidad=item.cantidad,
            precio_unitario=db_producto.precio
        )
        total += db_producto.precio * item.cantidad
        db.add(db_item)

    # Actualizar total
    db_pedido.total = total
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.patch("/{id}", response_model=PedidoResponse)
def update_pedido(id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = get_or_404(db, Pedido, id, "Pedido no encontrado")

    if pedido.id_cliente is not None:
        get_or_404(db, Cliente, pedido.id_cliente, "Cliente no encontrado")

    for key, value in pedido.model_dump(exclude_none=True).items():
        setattr(db_pedido, key, value)

    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.delete("/{id}", status_code=204)
def delete_pedido(id: int, db: Session = Depends(get_db)):
    db_pedido = get_or_404(db, Pedido, id, "Pedido no encontrado")
    db.delete(db_pedido)
    db.commit()