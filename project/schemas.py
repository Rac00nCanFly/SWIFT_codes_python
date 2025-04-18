from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

class SwiftCodeBase(BaseModel):
    swift_code: str
    bank_name: str
    address: str
    country_iso2: str
    country_name: str
    is_headquarter: bool

    # Konfiguracja camelCase dla JSON
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,  # pozwala używać snake_case w Pythonie
        from_attributes=True
    )

class SwiftCodeCreate(SwiftCodeBase):
    pass

class SwiftCodeResponse(SwiftCodeBase):
    branches: list["SwiftCodeResponse"] = []

class CountrySwiftCodes(BaseModel):
    country_iso2: str
    country_name: str
    swift_codes: list[SwiftCodeResponse]

class MessageResponse(BaseModel):
    message: str




