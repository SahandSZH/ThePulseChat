from fastapi import FastAPI
from database import Base, engine
from routers import group
app = FastAPI()

# Create the tables if they don't exist already
Base.metadata.create_all(bind=engine)

app.include_router(group.router)