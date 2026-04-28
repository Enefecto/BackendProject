from sqlalchemy import Column, Integer, String
from app.db import Base
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String, unique=True)

    pedidos = relationship("Pedido", back_populates="cliente")