from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True
