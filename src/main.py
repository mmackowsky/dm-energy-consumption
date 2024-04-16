from typing import List

import uvicorn
from fastapi import FastAPI, Query, status

from config import get_settings
from schemas import EnergyConsumption
from utils import get_user_id

settings = get_settings()
app = FastAPI()


@app.get("/api/energy", status_code=status.HTTP_200_OK)
async def get_measurements():
    return get_user_id()


@app.get(
    "/api/energy/{date}",
    status_code=status.HTTP_200_OK,
)
def get_measurements(date):
    pass


@app.delete("/api/energy/{id}", status_code=status.HTTP_200_OK)
async def delete_measurement(id):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
