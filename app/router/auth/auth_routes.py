from fastapi import APIRouter, HTTPException, status,Depends
from app.schemas.user_schema import UserCreate, UserLogin, Token, UserPublic
from app.database import user_collection
from app.core.auth import hash_password, verify_password, create_access_token
from app.model.user_model import Role
from bson import ObjectId
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserPublic)
async def register(user: UserCreate):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hash_password(user.password),
        "role": Role.junior,
    }
    result = await user_collection.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    return UserPublic(
        id=str(new_user["_id"]),
        email=new_user["email"],
        name=new_user["name"],
        role=new_user["role"]
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await user_collection.find_one({"email": form_data.username})
    if not db_user or not verify_password(form_data.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({
        "sub": str(db_user["_id"]),
        "email": db_user["email"],
        "role": db_user["role"]
    })
    return {"access_token": token, "token_type": "bearer"}
