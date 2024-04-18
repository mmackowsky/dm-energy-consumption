from fastapi import Request
from sqlalchemy import desc

from config import get_settings
from database import SessionLocal
from models import EnergyConsumption

settings = get_settings()


def set_new_id(db: SessionLocal):
    last_object_id = (
        db.query(EnergyConsumption).order_by(desc(EnergyConsumption.id)).first()
    )
    next_id = (last_object_id.id + 1) if last_object_id.id else 1
    return next_id
