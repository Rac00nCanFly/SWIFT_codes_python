
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi_redis_cache import FastApiRedisCache
from sqlalchemy.orm import Session
from project.database import get_db, engine
from project import models, schemas
from project.monitoring import add_monitoring

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.getenv("TESTING"):
        redis_cache = FastApiRedisCache()
        redis_cache.init(
            host_url=os.getenv("REDIS_URL", "redis://redis:6379"),
            prefix="swift-cache",
            response_header="X-SWIFT-Cache",
            ignore_arg_types=[Session]
        )
    
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="SWIFT Codes API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc"
)

@app.get(
    "/v1/swift-codes/{swift_code}",
    response_model=schemas.SwiftCodeResponse,
    response_model_by_alias=True
)
async def get_swift_code(
    swift_code: str,
    db: Session = Depends(get_db)
):
    swift_code = swift_code.upper()
    db_swift = db.get(models.SwiftCode, swift_code)
    
    if not db_swift:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    
    response = schemas.SwiftCodeResponse.model_validate(db_swift)
    
    if db_swift.is_headquarter:
        branches = db.query(models.SwiftCode).filter(
            models.SwiftCode.swift_code.like(f"{swift_code[:8]}%"),
            models.SwiftCode.swift_code != swift_code
        ).all()
        response.branches = [schemas.SwiftCodeBase.model_validate(b) for b in branches]
    
    return response

@app.get(
    "/v1/swift-codes/country/{country_iso2}",
    response_model=schemas.CountrySwiftCodesResponse,
    response_model_by_alias=True
)
async def get_country_swift_codes(
    country_iso2: str,
    db: Session = Depends(get_db)
):
    country_iso2 = country_iso2.upper()
    swift_codes = db.query(models.SwiftCode).filter(
        models.SwiftCode.country_iso2 == country_iso2
    ).all()
    
    if not swift_codes:
        raise HTTPException(status_code=404, detail="No SWIFT codes found for this country")
    
    return schemas.CountrySwiftCodesResponse(
        country_iso2=country_iso2,
        country_name=swift_codes[0].country_name,
        swift_codes=swift_codes
    )

@app.post(
    "/v1/swift-codes",
    response_model=schemas.MessageResponse,
    status_code=201
)
async def create_swift_code(
    data: schemas.SwiftCodeCreate,
    db: Session = Depends(get_db)
):
    data_dict = data.model_dump(by_alias=True)
    swift_code = data_dict["swiftCode"].upper()
    
    if db.get(models.SwiftCode, swift_code):
        raise HTTPException(
            status_code=400,
            detail=f"SWIFT code {swift_code} already exists"
        )
    
    db_swift = models.SwiftCode(
        swift_code=swift_code,
        bank_name=data_dict["bankName"],
        address=data_dict["address"],
        country_iso2=data_dict["countryISO2"].upper(),
        country_name=data_dict["countryName"].upper(),
        is_headquarter=data_dict["isHeadquarter"]
    )
    
    db.add(db_swift)
    db.commit()
    return {"message": "SWIFT code created successfully"}

@app.delete(
    "/v1/swift-codes/{swift_code}",
    response_model=schemas.MessageResponse
)
async def delete_swift_code(
    swift_code: str,
    db: Session = Depends(get_db)
):
    swift_code = swift_code.upper()
    db_swift = db.get(models.SwiftCode, swift_code)
    
    if not db_swift:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    
    db.delete(db_swift)
    db.commit()
    return {"message": "SWIFT code deleted successfully"}

add_monitoring(app)
