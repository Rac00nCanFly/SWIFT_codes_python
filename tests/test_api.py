import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.main import app
from project.database import Base

client = TestClient(app)

@pytest.fixture(scope="function")
def clean_db():
    from project.models import Base
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    yield Session()
    
    Base.metadata.drop_all(engine)


def test_create_and_get_swift_code(clean_db):
    test_data = {
        "swift_code": "TESTCODEXXX",
        "bank_name": "Test Bank",
        "address": "Test Address",
        "country_iso2": "PL",
        "country_name": "Poland",
        "is_headquarter": True
    }
    
    
    response = client.post("/v1/swift-codes", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code created successfully"}

    
    response = client.get("/v1/swift-codes/TESTCODEXXX")
    assert response.status_code == 200
    assert response.json()["swiftCode"] == "TESTCODEXXX"
    assert response.json()["bankName"] == "Test Bank"     
    assert response.json()["isHeadquarter"] is True       

def test_delete_swift_code(clean_db):
    test_data = {
        "swift_code": "TESTCODEXXX",
        "bank_name": "Test Bank",
        "address": "Test Address",
        "country_iso2": "PL",
        "country_name": "Poland",
        "is_headquarter": True
    }
    
    client.post("/v1/swift-codes", json=test_data)
 
    response = client.delete("/v1/swift-codes/TESTCODEXXX")
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code deleted successfully"}
  
    response = client.get("/v1/swift-codes/TESTCODEXXX")
    assert response.status_code == 404

def test_get_country_swift_codes(clean_db):
    
    client.post("/v1/swift-codes", json={
        "swift_code": "BANKPLPWXXX",
        "bank_name": "Bank HQ",
        "address": "Warsaw",
        "country_iso2": "PL",
        "country_name": "POLAND",
        "is_headquarter": True
    })
    client.post("/v1/swift-codes", json={
        "swift_code": "BANKPLPW001",
        "bank_name": "Bank Branch",
        "address": "Krakow",
        "country_iso2": "PL",
        "country_name": "POLAND",
        "is_headquarter": False
    })
    
    response = client.get("/v1/swift-codes/country/PL")
    assert response.status_code == 200
    data = response.json()
    assert data["countryISO2"] == "PL"
    assert len(data["swiftCodes"]) == 2

def test_create_duplicate_swift_code(clean_db):
    test_data = {
        "swift_code": "DUPLICATEXXX",
        "bank_name": "Bank",
        "address": "Address",
        "country_iso2": "PL",
        "country_name": "POLAND",
        "is_headquarter": True
    }
    response1 = client.post("/v1/swift-codes", json=test_data)
    assert response1.status_code == 200
    response2 = client.post("/v1/swift-codes", json=test_data)
    assert response2.status_code in [400, 409]

def test_get_nonexistent_swift_code(clean_db):
    response = client.get("/v1/swift-codes/NOTEXIST123")
    assert response.status_code == 404

def test_delete_nonexistent_swift_code(clean_db):
    response = client.delete("/v1/swift-codes/NOTEXIST123")
    assert response.status_code == 404
