from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)

    locations = relationship("Location", back_populates="client")

    def __repr__(self):
        return f"<Client {self.name}, {self.email}, {self.phone}>"


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost_per_day = Column(DECIMAL(10, 2))
    is_available = Column(Boolean, default=True)

    locations = relationship("Location", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment {self.name}>"


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    id_client = Column(Integer, ForeignKey("clients.id"))
    id_equipment = Column(Integer, ForeignKey("equipments.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_returned = Column(Boolean, default=False)

    client = relationship("Client", back_populates="locations")
    equipment = relationship("Equipment", back_populates="locations")

    def __repr__(self):
        return f"<Location {self.id_client}, {self.id_equipment}>"
