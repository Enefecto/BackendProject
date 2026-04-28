from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String, nullable=False, default="En espera")
    total = Column(Float, nullable=False, default=0.0)
    fecha = Column(DateTime, server_default=func.now())
    id_cliente = Column(Integer, ForeignKey("clientes.id", ondelete="SET NULL"), nullable=True)

    cliente = relationship("Cliente", back_populates="pedidos")
    productos = relationship("PedidoProducto", back_populates="pedido", cascade="all, delete-orphan")