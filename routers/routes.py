from fastapi import APIRouter, Depends, HTTPException
from models.models import User
 
from dependencies import get_current_user

router = APIRouter()
#prefix='/dashboard', tags=['Protected']
@router.get('/admin')
def admin_route(current_user:User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return {"message": "Welcome to the admin dashboard", "user": current_user.username}
