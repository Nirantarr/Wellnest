# backend/routers/auth.py

# The corrected "After" for backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Change these lines
import models
import security
from database import db

# You'll likely need this for the User model response
from bson import ObjectId
from pydantic import EmailStr

router = APIRouter(
    tags=["Authentication"]
)

# MODIFIED /register endpoint
@router.post("/register", response_model=models.User)
async def register_user(user: models.UserCreate):
    # Check if user already exists
    db_user = db.users.find_one({"email": user.email})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = security.get_password_hash(user.password)
    
    # Prepare user data for MongoDB insertion
    user_data = {
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    # Save user to the "users" collection in the database
    result = db.users.insert_one(user_data)
    
    # Check if the insertion was successful
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Error creating user")
        
    # Return the created user's data (without the password)
    return {
        "full_name": user.full_name,
        "email": user.email
    }


# NO CHANGES NEEDED for the /login endpoint
@router.post("/login", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"email": form_data.username})
    if not user or not security.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": user["email"]}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}