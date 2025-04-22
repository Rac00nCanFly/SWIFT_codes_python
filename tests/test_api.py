import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.main import app
from project.database import get_db
from project import models

os.environ["TESTING"] = "1"

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:?cache=shared"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_and_get_swift_code(client):
    test_data = {
        "swiftCode": "TESTCODEXXX",
        "bankName": "Test Bank",
        "address": "Test Address",
        "countryISO2": "PL",
        "countryName": "Poland",
        "isHeadquarter": True
    }
    response = client.post("/v1/swift-codes", json=test_data)
    assert response.status_code == 201, response.text
    response = client.get("/v1/swift-codes/TESTCODEXXX")
    assert response.status_code == 200
    assert response.json()["swiftCode"] == "TESTCODEXXX"

def test_delete_swift_code(client):
    test_data = {
        "swiftCode": "DELETECODEXX",
        "bankName": "Delete Bank",
        "address": "Delete Address",
        "countryISO2": "DE",
        "countryName": "Germany",
        "isHeadquarter": True
    }
    client.post("/v1/swift-codes", json=test_data)
    response = client.delete("/v1/swift-codes/DELETECODEXX")
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code deleted successfully"}
    response = client.get("/v1/swift-codes/DELETECODEXX")
    assert response.status_code == 404

def test_get_country_swift_codes(client):

    client.post("/v1/swift-codes", json={
        "swiftCode": "BANKPLPWXXX",
        "bankName": "Bank HQ",
        "address": "Warsaw",
        "countryISO2": "PL",
        "countryName": "POLAND",
        "isHeadquarter": True
    })
    client.post("/v1/swift-codes", json={
        "swiftCode": "BANKPLPW001",
        "bankName": "Bank Branch",
        "address": "Krakow",
        "countryISO2": "PL",
        "countryName": "POLAND",
        "isHeadquarter": False
    })

    response = client.get("/v1/swift-codes/country/PL")
    assert response.status_code == 200
    data = response.json()
    assert data["countryISO2"] == "PL"
    assert data["countryName"] == "POLAND"
    assert len(data["swiftCodes"]) == 2

def test_create_duplicate_swift_code(client):
    test_data = {
        "swiftCode": "DUPLICATEXXX",
        "bankName": "Bank",
        "address": "Address",
        "countryISO2": "PL",
        "countryName": "POLAND",
        "isHeadquarter": True
    }
    response = client.post("/v1/swift-codes", json=test_data)
    assert response.status_code == 201
    response = client.post("/v1/swift-codes", json=test_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_nonexistent_swift_code(client):
    response = client.get("/v1/swift-codes/NOTEXIST123")
    assert response.status_code == 404

def test_delete_nonexistent_swift_code(client):
    response = client.delete("/v1/swift-codes/NOTEXIST123")
    assert response.status_code == 404
