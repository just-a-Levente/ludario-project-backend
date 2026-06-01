from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.tables import Base
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

# ---------------------
# FOR BOARDGAMES AND USER INFO
# ---------------------

DATABASE_URL = "postgresql+psycopg2://admin:oPsox7FVja3txd14PLdeDwsJEXlPQGRn@dpg-d8evp3pkh4rs73enunpg-a.frankfurt-postgres.render.com/ludario_0y4l"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# ---------------------
# FOR CHAT MESSAGES
# ---------------------

MONGO_URL = "mongodb+srv://lekovacs789_db_user:4gMA0PcncvOBDq7X@ludario-chat.rffissh.mongodb.net/?appName=ludario-chat"
MONGO_DB_NAME = "ludario_chat"

mongo_client = AsyncMongoClient(MONGO_URL, server_api=ServerApi('1'))
mongo_db = mongo_client[MONGO_DB_NAME]
messages_collection = mongo_db["messages"]