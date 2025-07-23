from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    role: str  # 🔒 No password here (for responses)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # 🔐 For input during register/login

class Token(BaseModel):
    access_token: str
    token_type: str
class Users(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None  # 🔐 For input during update