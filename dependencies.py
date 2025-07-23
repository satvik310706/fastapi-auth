from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from models.models import User
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail='Invalid token')
        # Fetch user from MongoDB
        from database import user_collection
        user = await user_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail='User not found')
        return User(email=user["email"], username=user["username"], role=user["role"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
