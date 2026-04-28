from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    id_vendedor: int

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    id_vendedor: Optional[int] = None

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True