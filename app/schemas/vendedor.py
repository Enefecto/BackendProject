from pydantic import BaseModel
from typing import Optional

class VendedorBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    zona: Optional[str] = None

class VendedorCreate(VendedorBase):
    pass

class VendedorUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    zona: Optional[str] = None

class VendedorResponse(VendedorBase):
    id: int

    class Config:
        from_attributes = True
