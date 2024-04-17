from fastapi import Header, HTTPException, Request, status
from jwt import PyJWTError, decode
from sqlalchemy import desc

from config import get_settings
from database import SessionLocal
from models import EnergyConsumption

settings = get_settings()


async def get_user_id(request: Request):
    user_id = request.headers.get("request-user-id")
    return user_id


def set_new_id(db: SessionLocal):
    last_object_id = (
        db.query(EnergyConsumption).order_by(desc(EnergyConsumption.id)).first()
    )
    next_id = (last_object_id.id + 1) if last_object_id.id else 1
    return next_id
