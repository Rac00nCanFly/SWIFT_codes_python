from sqlalchemy import Column, String, Boolean, ForeignKey,Index
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class SwiftCode(Base):
    __tablename__ = "swift_codes"
    swift_code = Column(String(11), primary_key=True)
    bank_name = Column(String)
    address = Column(String)
    country_iso2 = Column(String(2))
    country_name = Column(String)
    is_headquarter = Column(Boolean)
    parent_code = Column(String(11), ForeignKey("swift_codes.swift_code"))
    __table_args__ = (
        Index("ix_swift_code", "swift_code"),
        Index("ix_country_iso2", "country_iso2"),
    )
    branches = relationship(
        "SwiftCode",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    parent = relationship(
        "SwiftCode",
        remote_side=[swift_code],
        back_populates="branches"
    )
