from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PedidoProductoBase(BaseModel):
    id_producto: int
    cantidad: int = 1

class PedidoProductoCreate(PedidoProductoBase):
    pass

class PedidoProductoResponse(PedidoProductoBase):
    id: int
    precio_unitario: float

    class Config:
        from_attributes = True

class PedidoBase(BaseModel):
    id_cliente: Optional[int] = None

class PedidoCreate(PedidoBase):
    productos: List[PedidoProductoCreate]

class PedidoUpdate(BaseModel):
    estado: Optional[str] = None
    id_cliente: Optional[int] = None

class PedidoResponse(PedidoBase):
    id: int
    estado: str
    total: float
    fecha: datetime
    productos: List[PedidoProductoResponse]

    class Config:
        from_attributes = True