import uvicorn
from fastapi import FastAPI, status

from config import get_settings

settings = get_settings()
app = FastAPI()


@app.get("/api/energy", status_code=status.HTTP_200_OK)
async def get_energy():
    return {"energy": "foo"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
