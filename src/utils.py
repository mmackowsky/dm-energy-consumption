from fastapi import Header, HTTPException, Request, status
from jwt import PyJWTError, decode

from config import get_settings

settings = get_settings()


async def get_user_id(request: Request):
    user_id = request.headers.get("request-user-id")
    return user_id
