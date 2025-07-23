from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL ="mongodb+srv://Satvik:Satvik%40310706@satvik.melxkhp.mongodb.net/?retryWrites=true&w=majority&appName=satvik"
client = AsyncIOMotorClient(MONGO_URL)
db = client["fast_auth"]
user_collection = db["users"]
