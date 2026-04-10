from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)