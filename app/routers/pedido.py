from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.pedido import Pedido
from app.models.pedido_producto import PedidoProducto
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoResponse, PedidoProductoCreate
from app.utils.helpers import get_or_404
from typing import List

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"]
)

ESTADOS_VALIDOS = ["En espera", "Preparando", "Terminado", "Enviado", "Entregado", "Cancelado"]

def validar_estado_modificable(pedido):
    if pedido.estado != "En espera":
        raise HTTPException(
            status_code=400,
            detail=f"No se puede modificar un pedido en estado '{pedido.estado}'"
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
    db.flush()

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

    # Validar estado
    if pedido.estado:
        if pedido.estado not in ESTADOS_VALIDOS:
            raise HTTPException(status_code=400, detail=f"Estado inválido, los estados válidos son: {ESTADOS_VALIDOS}")
        if db_pedido.estado != "En espera" and pedido.estado == "Cancelado":
            raise HTTPException(status_code=400, detail="Solo se puede cancelar un pedido en estado 'En espera'")

    # Validar cliente
    if pedido.id_cliente is not None:
        validar_estado_modificable(db_pedido)
        get_or_404(db, Cliente, pedido.id_cliente, "Cliente no encontrado")

    for key, value in pedido.model_dump(exclude_none=True).items():
        setattr(db_pedido, key, value)

    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.post("/{id}/productos", response_model=PedidoResponse, status_code=201)
def add_producto_pedido(id: int, item: PedidoProductoCreate, db: Session = Depends(get_db)):
    db_pedido = get_or_404(db, Pedido, id, "Pedido no encontrado")
    validar_estado_modificable(db_pedido)

    db_producto = get_or_404(db, Producto, item.id_producto, "Producto no encontrado")

    db_item = PedidoProducto(
        id_pedido=db_pedido.id,
        id_producto=item.id_producto,
        cantidad=item.cantidad,
        precio_unitario=db_producto.precio
    )
    db_pedido.total += db_producto.precio * item.cantidad
    db.add(db_item)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.delete("/{id}/productos/{id_producto}", response_model=PedidoResponse)
def remove_producto_pedido(id: int, id_producto: int, db: Session = Depends(get_db)):
    db_pedido = get_or_404(db, Pedido, id, "Pedido no encontrado")
    validar_estado_modificable(db_pedido)

    db_item = db.query(PedidoProducto).filter(
        PedidoProducto.id_pedido == id,
        PedidoProducto.id_producto == id_producto
    ).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el pedido")

    db_pedido.total -= db_item.precio_unitario * db_item.cantidad
    db.delete(db_item)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@router.delete("/{id}", status_code=204)
def delete_pedido(id: int, db: Session = Depends(get_db)):
    db_pedido = get_or_404(db, Pedido, id, "Pedido no encontrado")
    db.delete(db_pedido)
    db.commit()