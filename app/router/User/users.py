from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.database import user_collection
from app.schemas.user_schema import UserPublic
from app.core.auth import get_current_user
from app.model.user_model import Role

router = APIRouter(prefix="/users", tags=["Users"])

@router.patch("/{user_id}/promote", response_model=UserPublic)
async def promote_user_role(
    user_id: str,
    new_role: Role,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != Role.superadmin:
        raise HTTPException(status_code=403, detail="Only superadmin can promote users")

    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": new_role.value}}
    )

    return UserPublic(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        role=new_role.value
    )
