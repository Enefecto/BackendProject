from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    id_vendedor = Column(Integer, ForeignKey("vendedores.id", ondelete="CASCADE"), nullable=False)

    vendedor = relationship("Vendedor", back_populates="productos")
    pedidos = relationship("PedidoProducto", back_populates="producto")