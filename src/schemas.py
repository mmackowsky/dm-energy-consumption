from pydantic import BaseModel


class EnergyConsumption(BaseModel):
    id: int
    measurement_date: str
    consumption: float

    def __str__(self):
        return "%s %s: %s" % (self.id, self.measurement_date, self.consumption)
