# backend/models.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

# New model for registration to include full_name and confirm_password
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    # This is the critical line. It must have max_length=70
    password: str = Field(..., min_length=6, max_length=70) 
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

# Updated User model to include more profile data
class User(BaseModel):
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True

# No changes needed for these models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None