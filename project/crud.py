from sqlalchemy.orm import Session
from .models import SwiftCode 

def get_swift_code(db: Session, swift_code: str):
    return db.query(SwiftCode).filter(SwiftCode.swift_code == swift_code).first()