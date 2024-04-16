from fastapi import Header, HTTPException, status
from jwt import PyJWTError, decode

from config import get_settings

settings = get_settings()


async def get_user_id(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload["id"]
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
