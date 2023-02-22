from fastapi import FastAPI, Depends
from app.v1 import api
from app.core.models.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api.router)



