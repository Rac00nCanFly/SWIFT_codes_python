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
    
    # Test tworzenia
    response = client.post("/v1/swift-codes", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code created successfully"}

    # Test pobierania
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
    
    # Utwórz rekord
    client.post("/v1/swift-codes", json=test_data)
    
    # Test usuwania
    response = client.delete("/v1/swift-codes/TESTCODEXXX")
    assert response.status_code == 200
    assert response.json() == {"message": "SWIFT code deleted successfully"}
    
    # Weryfikacja usunięcia
    response = client.get("/v1/swift-codes/TESTCODEXXX")
    assert response.status_code == 404
