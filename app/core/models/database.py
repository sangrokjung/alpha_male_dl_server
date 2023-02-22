from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os, sys
from dotenv import load_dotenv

load_dotenv()
#psqlPath = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}/{os.getenv('DB_DATABASE')} s"
print(os.getenv('DATABASE_URL'))

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

