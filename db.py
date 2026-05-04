from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.tables import Base

DATABASE_URL = "postgresql+psycopg2://postgres:Leti_2004@localhost:5432/ludario"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)