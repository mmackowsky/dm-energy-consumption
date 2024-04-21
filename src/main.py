from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status

from config import get_settings
from database import SessionLocal, engine
from models import EnergyConsumption
from utils import set_new_id
from worker import periodic_task, add_energy_consumption

settings = get_settings()
app = FastAPI()
db = SessionLocal()


# REMOVE IN FINAL VERSION
@app.post("/api/fake-measurement", status_code=status.HTTP_201_CREATED)
async def fake_measurement(request: Request):
    user_id = int(request.headers.get("request-user-id"))
    energy_consumption = EnergyConsumption(
        id=set_new_id(db),
        user=user_id,
        energy_consumption=100,
        measurement_date=datetime.now().strftime("%d-%m-%Y"),
    )
    db.add(energy_consumption)
    db.commit()
    db.refresh(energy_consumption)
    return energy_consumption


@app.post("/api/energy/collect-data", status_code=status.HTTP_201_CREATED)
async def collect_data(request: Request):
    user_id = request.headers.get("request-user-id")
    print(user_id)
    data = add_energy_consumption.delay(user_id=user_id)
    print(data)
    return data


@app.get("/api/energy", status_code=status.HTTP_200_OK)
async def get_energy_consumptions(request: Request):
    return db.query(EnergyConsumption).all()


@app.get(
    "/api/energy/{measurement_id}",
    status_code=status.HTTP_200_OK,
)
def get_energy_consumption_by_id(request: Request, measurement_id: int):
    return (
        db.query(EnergyConsumption)
        .filter(EnergyConsumption.id == measurement_id)
        .first()
    )


@app.delete("/api/energy/{measurement_id}", status_code=status.HTTP_200_OK)
async def delete_measurement(measurement_id: int):
    measurement = (
        db.query(EnergyConsumption)
        .filter(EnergyConsumption.id == measurement_id)
        .first()
    )
    if not measurement:
        raise HTTPException(
            detail="Measurement not found", status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(measurement)
    db.commit()
    return {"message": "Measurement deleted"}


if __name__ == "__main__":
    EnergyConsumption.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
