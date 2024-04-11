import uvicorn
from fastapi import FastAPI

from config import get_settings

settings = get_settings()
app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
