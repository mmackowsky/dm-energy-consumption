from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, Query, status
from pymongo import MongoClient

import database
from config import get_settings
from schemas import EnergyConsumption

settings = get_settings()
app = FastAPI()
client = MongoClient()
collection = client[settings.DB_NAME][settings.DB_COLLECTION]


@app.get("/api/energy", status_code=status.HTTP_200_OK)
async def get_measurements():
    measurements = collection.find({})
    return measurements


@app.get(
    "/measurements/",
    response_model=List[EnergyConsumption],
    status_code=status.HTTP_200_OK,
)
def get_measurements(date: datetime = Query(...)):
    """Get measurements from a specific date."""
    start_of_day = datetime.combine(date.date(), datetime.min.time())
    end_of_day = datetime.combine(date.date(), datetime.max.time())
    query = {"date": {"$gte": start_of_day, "$lte": end_of_day}}
    measurements = list(collection.find(query))
    return measurements


@app.delete("/api/energy/{id}", status_code=status.HTTP_200_OK)
async def delete_measurement(id):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
