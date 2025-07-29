from fastapi import APIRouter, Depends, HTTPException,Form
from datetime import datetime, timedelta
from app.schemas.user_schema import  AttendancePublic
from app.model.user_model import AttendanceIn,AttendanceStatus
from app.database import attendance_collection,user_collection
from app.core.auth import get_current_user  
from datetime import datetime, date
from typing import List
from pytz import timezone
from bson import ObjectId
import logging

router = APIRouter(tags=["Attendance"])

logger = logging.getLogger(__name__)
# Set IST timezone
IST = timezone("Asia/Kolkata")


@router.get("/peruser-attendance-record", response_model=List[AttendancePublic])
async def get_my_attendance(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])

    cursor = attendance_collection.find({"user_id": user_id})
    records = []

    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        records.append(doc)

    return records

@router.post("/mark-our-attendance")
async def mark_attendance(
    status: AttendanceStatus = Form(...),
    current_user: dict = Depends(get_current_user)
):
    now = datetime.now(IST)
    time = now.strftime("%d %B %Y, %I:%M %p")  
    date_str = now.strftime("%Y-%m-%d")        

    user_id = str(current_user["_id"])
    user_name = current_user["name"]

    # ✅ Check if already marked today by (user_id + date)
    existing = await attendance_collection.find_one({
        "user_id": user_id,
        "date": date_str
    })

    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked today")

    attendance_data = {
        "user_id": user_id,
        "user_name": user_name,
        "status": status.value,
        "time": time,        
        "date": date_str     
    }

    await attendance_collection.insert_one(attendance_data)
    return {"message": "Attendance marked", "status": status.value}

from app.utils.cache_data import custom_cache

@router.get("/users_attendance_record", response_model=List[AttendancePublic])
@custom_cache(ttl=120)
async def get_all_attendance(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can access all attendance data")
    cursor = attendance_collection.find({})
    records = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["user_id"] = str(doc["user_id"])
        user = await user_collection.find_one({"_id": ObjectId(doc["user_id"])})
        doc["user_name"] = user["name"] if user else "Unknown"
        records.append(doc)

    return records
