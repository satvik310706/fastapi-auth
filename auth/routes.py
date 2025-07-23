from fastapi import APIRouter, HTTPException
from models.models import User, UserCreate, Token, Users
from services.services import authenticate_user, register_user, get_all_user, get_user_by_id, update_user_by_id, delete_by_id
from auth.utils import create_access_token

router = APIRouter()
#prefix="/auth", tags=["Auth"]
@router.post("/register", response_model=User)
async def register(user: UserCreate):
    user_data = user.dict()
    created_user = await register_user(user_data)
    if not created_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return created_user

@router.post("/login", response_model=Token)
async def login(email: str, password: str):
    user_data = await authenticate_user(email, password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": user_data["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=list[User])
async def get_users():
    return await get_all_user()

@router.get('/{user_id}', response_model=User)
async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put('/{user_id}',response_model=Users)
async def update_user(user_id:str, user_data : Users):
    user_info = await update_user_by_id(user_id, user_data.dict(exclude_unset=True))
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info

@router.delete('/{user_id}')
async def delete_user(user_id: str):
    user = await delete_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user