from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from enum import Enum

class Role(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    manager = "manager"
    junior = "junior"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.hr_system
user_collection = db.get_collection("users")

async def create_superadmin():
    email = "khushipandey8292@gmail.com"
    existing = await user_collection.find_one({"email": email})
    if existing:
        print("❗ Superadmin already exists.")
        return

    user = {
        "email": email,
        "name": "khushi",
        "hashed_password": pwd_context.hash("khushi@123"),
        "role": Role.superadmin.value,
    }
    await user_collection.insert_one(user)
    print("✅ Superadmin created.")

# Run this manually using asyncio
if __name__ == "__main__":
    import asyncio
    asyncio.run(create_superadmin())
