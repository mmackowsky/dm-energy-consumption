import unittest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings
from database import get_db
from main import app
from models import EnergyConsumption

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


EnergyConsumption.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestEnergyAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.client = TestClient(app)
        db = TestingSessionLocal()
        energy = EnergyConsumption(
            id=1,
            user=1,
            measurement_date=datetime.now().strftime("%Y-%m-%d"),
            energy_consumption=100,
        )
        db.add(energy)
        db.commit()
        db.refresh(energy)
        db.close()

    def tearDown(self):
        db = TestingSessionLocal()
        db.query(EnergyConsumption).delete()
        db.commit()
        db.close()

    def test_get_energy_consumption(self):
        response = self.client.get("/api/energy")
        print(response.json())
        print(response.text)
        print(response.status_code)

    def test_get_energy_consumptions(self):
        response = self.client.get("/api/energy")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_get_energy_consumption_by_id(self):
        response = self.client.get("/api/energy/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_delete_energy_measurement(self):
        response = self.client.delete("/api/energy/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_delete_nonexistent_energy_measurement(self):
        response = self.client.delete("/api/energy/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
