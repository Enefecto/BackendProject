from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class PedidoProducto(Base):
    __tablename__ = "pedido_producto"

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False)
    id_pedido = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id", ondelete="RESTRICT"), nullable=False)

    pedido = relationship("Pedido", back_populates="productos")
    producto = relationship("Producto", back_populates="pedidos")