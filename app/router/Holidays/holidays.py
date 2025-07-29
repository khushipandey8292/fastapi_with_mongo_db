from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import HolidayCreate, HolidayPublic
from app.database import holiday_collection
from app.core.auth import get_current_user
from app.model.user_model import Role
from bson import ObjectId

router = APIRouter(prefix="/holidays", tags=["Holiday"])

@router.post("/", response_model=HolidayPublic)
async def create_holiday(
    data: HolidayCreate,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != Role.superadmin:
        raise HTTPException(status_code=403, detail="Only superadmin can create holidays")

    existing = await holiday_collection.find_one({"date": str(data.date)})
    if existing:
        raise HTTPException(status_code=400, detail="Holiday already exists for this date")

    result = await holiday_collection.insert_one({
        "date": str(data.date),
        "reason": data.reason
    })

    return HolidayPublic(id=str(result.inserted_id), date=data.date, reason=data.reason)

# ✅ Anyone can view holidays
@router.get("/holidays")
async def list_holidays():
    holidays_cursor = holiday_collection.find()
    holiday_list = []
    async for holiday in holidays_cursor:
        holiday_list.append({
            "date": holiday.get("date", ""),
            "reason": holiday.get("reason", "")
        })
    return holiday_list

