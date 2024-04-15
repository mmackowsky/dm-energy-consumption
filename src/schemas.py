from pydantic import BaseModel


class EnergyConsumption(BaseModel):
    id: int
    measurement_date: str
    consumption: float
