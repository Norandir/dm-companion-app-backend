# app/main.py
from fastapi import FastAPI
from app.db.models import Base
from app.db.session import engine
from app.api import campaigns, rules, notes

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()

# Include the routes defined in separate files (e.g., campaigns, rules)
app.include_router(campaigns.router)
app.include_router(rules.router)
app.include_router(notes.router)
