from database import user_collection
from auth.utils import get_password_hash, verify_password
from bson import ObjectId

def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

async def authenticate_user(email: str, password: str):
    user_data = await user_collection.find_one({"email": email})
    if user_data and verify_password(password, user_data["password"]):
        return serialize_user(user_data)
    return None

async def register_user(user: dict):
    if await user_collection.find_one({"email": user["email"]}):
        return None
    else:
        user["password"] = get_password_hash(user["password"])
        inserted = await user_collection.insert_one(user)
        created_user = await user_collection.find_one({"_id": inserted.inserted_id})
        return serialize_user(created_user)

async def get_all_user():
    users = []
    async for user in user_collection.find():
        users.append(serialize_user(user))
    return users
async def get_user_by_id(user_id:str):
    user_data = await user_collection.find_one({"_id":ObjectId(user_id)})
    if user_data:
        return serialize_user(user_data)
async def update_user_by_id(user_id:str, user_data:dict):
    user_datas = await user_collection.find_one({"_id":ObjectId(user_id)})
    if user_datas:
        await user_collection.update_one({"_id":ObjectId(user_id)},{"$set":user_data})
        return serialize_user(await user_collection.find_one({"_id":ObjectId(user_id)}))
async def delete_by_id(user_id:str):
    user_data = await user_collection.find_one({"_id":ObjectId(user_id)})
    if user_data:
        await user_collection.delete_one({"_id":ObjectId(user_id)})
        return {"info": "User deleted successfully"}