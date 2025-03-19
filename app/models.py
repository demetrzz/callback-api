from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    status = Column(String)
    product_id = Column(ForeignKey("products.id"))
    timestamp = Column(DateTime(timezone=True))
