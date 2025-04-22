from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_validator

class SwiftCodeBase(BaseModel):
    swift_code: str = Field(..., alias="swiftCode")
    bank_name: str = Field(..., alias="bankName")
    address: str = Field(...)
    country_iso2: str = Field(..., alias="countryISO2")
    country_name: str = Field(..., alias="countryName")
    is_headquarter: bool = Field(..., alias="isHeadquarter")

    @field_validator('swift_code', 'country_iso2', 'country_name', mode='before')
    def uppercase_fields(cls, value):
        return value.upper() if value else value

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class SwiftCodeCreate(SwiftCodeBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "swiftCode": "NEWCODEXXX",
                "bankName": "New Bank",
                "address": "Bank Street 123",
                "countryISO2": "US",
                "countryName": "UNITED STATES",
                "isHeadquarter": True
            }
        }
    )

class SwiftCodeResponse(SwiftCodeBase):
    branches: List["SwiftCodeBase"] = []

class CountrySwiftCodesResponse(BaseModel):
    country_iso2: str = Field(..., alias="countryISO2")
    country_name: str = Field(..., alias="countryName")
    swift_codes: List[SwiftCodeBase] = Field(..., alias="swiftCodes")

    @field_validator('country_iso2', 'country_name', mode='before')
    def uppercase_fields(cls, value):
        return value.upper() if value else value

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "countryISO2": "PL",
                "countryName": "POLAND",
                "swiftCodes": []
            }
        }
    )

class MessageResponse(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )

SwiftCodeResponse.model_rebuild()
