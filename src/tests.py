from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, EnergyConsumption

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency to override the database session
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


# Test cases
def test_collect_data():
    response = client.post("/api/energy/collect-data", headers={"request-user-id": "test_user"})
    assert response.status_code == 201
    assert response.json() is not None


def test_get_energy_consumptions():
    response = client.get("/api/energy")
    assert response.status_code == 200
    assert response.json() == []


def test_get_energy_consumption_by_id():
    # Assume there's a measurement in the database with id=1
    # Add test data to the database
    with get_test_db() as db:
        measurement = EnergyConsumption(id=1, user=1, measurement_date="25-02-2024", energy_consumption=666)  # Fill in with appropriate data
        db.add(measurement)
        db.commit()

    response = client.get("/api/energy/1")
    assert response.status_code == 200
    assert response.json() is not None


def test_delete_energy_measurement():
    # Assume there's a measurement in the database with id=1
    # Add test data to the database
    with get_test_db() as db:
        measurement = EnergyConsumption(id=1, user=1, measurement_date="25-02-2024", energy_consumption=666)  # Fill in with appropriate data
        db.add(measurement)
        db.commit()

    response = client.delete("/api/energy/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Measurement deleted"}

    # Check if the measurement is actually deleted
    with get_test_db() as db:
        deleted_measurement = db.query(EnergyConsumption).filter(EnergyConsumption.id == 1).first()
        assert deleted_measurement is None
