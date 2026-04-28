from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Vendedor(Base):
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String)
    zona = Column(String)

    productos = relationship("Producto", back_populates="vendedor", cascade="all, delete-orphan")