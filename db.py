from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.tables import Base
from motor.motor_asyncio import AsyncIOMotorClient

# ---------------------
# FOR BOARDGAMES AND USER INFO
# ---------------------

DATABASE_URL = "postgresql+psycopg2://postgres:Leti_2004@localhost:5432/ludario"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# ---------------------
# FOR CHAT MESSAGES
# ---------------------

MONGO_URL = "mongodb://localhost:27017"
MONGO_DB_NAME = "ludario_chat"

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB_NAME]
messages_collection = mongo_db["messages"]