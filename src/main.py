from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, Query, Request, status

from config import get_settings
from database import SessionLocal, engine
from models import EnergyConsumption
from utils import get_user_id

settings = get_settings()
app = FastAPI()
db = SessionLocal()


@app.get("/api/fake-measurement", status_code=status.HTTP_200_OK)
async def fake_measurement(request: Request):
    user_id = int(request.headers.get("request-user-id"))
    energy_consumption = EnergyConsumption(
        id=1, user=user_id, energy_consumption=100, measurement_date=datetime.now()
    )
    db.add(energy_consumption)
    db.commit()
    db.refresh(energy_consumption)
    return energy_consumption


@app.get("/api/energy", status_code=status.HTTP_200_OK)
async def get_measurements(request: Request):
    user_id = request.headers.get("request-user-id")
    print(user_id)
    return {"user": user_id}


@app.get(
    "/api/energy/{date}",
    status_code=status.HTTP_200_OK,
)
def get_measurement(request: Request, date):
    pass


@app.delete("/api/energy/{id}", status_code=status.HTTP_200_OK)
async def delete_measurement(id):
    pass


if __name__ == "__main__":
    EnergyConsumption.metadata.create_all(bind=engine)
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
