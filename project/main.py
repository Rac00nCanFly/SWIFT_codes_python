from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/v1/swift-codes/{swift_code}", response_model=schemas.SwiftCodeResponse)
def get_swift_code(swift_code: str, db: Session = Depends(get_db)):
    db_swift = db.query(models.SwiftCode).filter(models.SwiftCode.swift_code == swift_code).first()
    if not db_swift:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    
    return db_swift

@app.get("/v1/swift-codes/country/{country_iso2}", response_model=schemas.CountrySwiftCodes)
def get_country_swift_codes(country_iso2: str, db: Session = Depends(get_db)):
    codes = db.query(models.SwiftCode).filter(models.SwiftCode.country_iso2 == country_iso2).all()
    if not codes:
        raise HTTPException(status_code=404, detail="No codes found for this country")
    
    return {
        "country_iso2": country_iso2,
        "country_name": codes[0].country_name,
        "swift_codes": codes
    }

@app.post("/v1/swift-codes", response_model=schemas.MessageResponse)
def create_swift_code(swift_code: schemas.SwiftCodeCreate, db: Session = Depends(get_db)):
    existing_code = db.query(models.SwiftCode).filter(models.SwiftCode.swift_code == swift_code.swift_code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail="SWIFT code already exists")
    
    db_code = models.SwiftCode(**swift_code.model_dump())
    
    db.add(db_code)
    db.commit()
    return {"message": "SWIFT code created successfully"}

@app.delete("/v1/swift-codes/{swift_code}", response_model=schemas.MessageResponse)
def delete_swift_code(swift_code: str, db: Session = Depends(get_db)):
    db_code = db.query(models.SwiftCode).filter(models.SwiftCode.swift_code == swift_code).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    
    db.delete(db_code)
    db.commit()
    return {"message": "SWIFT code deleted successfully"}