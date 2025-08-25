from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

# client = AsyncIOMotorClient("mongodb://localhost:27017")
client = AsyncIOMotorClient("mongodb://mongo:27017")
# client = AsyncIOMotorClient("mongodb://host.docker.internal:27017/hr_system") 
db = client.hr_system
user_collection = db.get_collection("users")
attendance_collection = db.get_collection("attendance")
salary_collection = db.get_collection("salary")
holiday_collection = db.get_collection("holidays")

async def init_indexes():
    await user_collection.create_index([("email", ASCENDING)], unique=True)

    await attendance_collection.create_index(
    [("user_id", 1), ("date", 1)],
    unique=True
    )
    await salary_collection.create_index(
        [("user_id", ASCENDING), ("month", ASCENDING)],
        unique=True
    )
    await holiday_collection.create_index([("date", 1)], unique=True)