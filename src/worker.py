import random
import time
from datetime import datetime, timedelta

from celery import Celery, shared_task

from config import get_settings
from database import SessionLocal
from models import EnergyConsumption

settings = get_settings()
db = SessionLocal()

app = Celery("src")
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    broker_connection_retry_on_startup=True,
)

app.autodiscover_tasks()


@app.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@shared_task(name="add_energy_consumption")
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


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(days=1),
        add_energy_consumption.s(),
        name="add_energy_consumption_every_24_hours",
    )


@app.task(name="tasks.periodic_task", bind=True, ignore_result=True)
def periodic_task(self):
    """
    Test task set to 5 minutes
    :return:
    """
    add_energy_consumption.apply_async(countdown=300, retry=False)
    return "Periodic task scheduled"
