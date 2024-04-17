import os
import random
import time
from datetime import datetime, timedelta

from celery import Celery

from config import get_settings
from database import SessionLocal, engine
from src.models import EnergyConsumption

settings = get_settings()
db = SessionLocal()

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="add_energy_consumption")
def add_energy_consumption(user_id):
    session = SessionLocal()
    try:
        # Losowa energia z zakresu 100 do 1000 kWh
        energy_consumption = random.randint(100, 1000)
        measurement_date = datetime.now().strftime("%Y-%m-%d")
        energy = EnergyConsumption(
            user=user_id,  # ID użytkownika, do zastąpienia przez rzeczywistego użytkownika
            measurement_date=measurement_date,
            energy_consumption=energy_consumption,
        )
        session.add(energy)
        session.commit()
    finally:
        session.close()


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(days=1),
        add_energy_consumption.s(),
        name="add_energy_consumption_every_24_hours",
    )
