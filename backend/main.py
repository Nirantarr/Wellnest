# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ConnectionFailure

from database import client

app = FastAPI()

# Define the origins that are allowed to make requests
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the WellNest AI Mental Health Companion API"}

@app.get("/test-db")
def test_database_connection():
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return {"status": "success", "message": "Successfully connected to MongoDB!"}
    except ConnectionFailure as e:
        # If connection fails, raise an HTTP exception
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")