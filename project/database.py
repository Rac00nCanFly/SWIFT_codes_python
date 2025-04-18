from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base 

engine = create_engine("sqlite:///./swift.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


