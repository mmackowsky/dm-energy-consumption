from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from database import Base


class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, nullable=False)
    measurement_date = Column(String, nullable=False)
    energy_consumption = Column(Integer, nullable=False)
