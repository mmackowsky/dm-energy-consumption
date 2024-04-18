import random
import time
from datetime import datetime, timedelta

from celery import Celery

from config import get_settings
from database import SessionLocal
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
        energy_consumption = random.randint(100, 1000)
        measurement_date = datetime.now().strftime("%Y-%m-%d")
        energy = EnergyConsumption(
            user=user_id,
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


@celery.task(name="tasks.periodic_task", bind=True, ignore_result=True)
def periodic_task():
    """
    Test task set to 5 minutes
    :return:
    """
    add_energy_consumption.apply_async(countdown=300, retry=False)
    return "Periodic task scheduled"
