from fastapi import APIRouter, Depends
from datetime import datetime, date
from app.database import attendance_collection, salary_collection, holiday_collection
from app.core.auth import get_current_user
from bson import ObjectId
import calendar
from app.tasks.send_email import send_salary_email  # Make sure this import is correct

router = APIRouter(tags=["salary"])

@router.get("/calculate-salary")
async def calculate_salary(current_user: dict = Depends(get_current_user)):
    now = datetime.now()
    year = now.year
    month = now.month

    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1)
    else:
        last_day = date(year, month + 1, 1)

    user_id = str(current_user["_id"])
    total_days = calendar.monthrange(year, month)[1]
    per_day_salary = 1000
    total_salary = 0
    holidays = set()
    
    # Fetch holidays for the month
    cursor = holiday_collection.find({
        "date": {"$regex": f"^{year}-{month:02d}"}
    })
    async for h in cursor:
        holidays.add(h["date"])

    present_days = set()

    # Fetch attendance records for the user in the given month
    cursor = attendance_collection.find({
        "user_id": user_id,
        "date": {"$gte": str(first_day), "$lt": str(last_day)}
    })
    async for doc in cursor:
        date_str = doc["date"]
        status = doc.get("status", "")
        present_days.add(date_str)

        if status in ("present", "cl", "short_day"):
            total_salary += per_day_salary
        elif status == "hdl":
            total_salary += per_day_salary * 0.5
        elif status in ("fdl", "lwp"):
            total_salary += 0

    # Add salary for holidays not marked as leave
    for day in range(1, total_days + 1):
        day_str = f"{year}-{month:02d}-{day:02d}"
        if day_str in holidays and day_str not in present_days:
            total_salary += per_day_salary

    # Prepare salary record
    salary_record = {
        "user_id": user_id,
        "user_name": current_user["name"],
        "month": f"{year}-{month:02d}",
        "total_salary": total_salary,
        "calculated_at": datetime.utcnow()
    }

    # Insert or update salary record
    existing = await salary_collection.find_one({
        "user_id": user_id,
        "month": f"{year}-{month:02d}"
    })

    if existing:
        await salary_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": salary_record}
        )
        salary_record["_id"] = str(existing["_id"])
    else:
        result = await salary_collection.insert_one(salary_record)
        salary_record["_id"] = str(result.inserted_id)

    # Trigger background email task via Celery
    send_salary_email.delay(
        to_email=current_user["email"],
        name=current_user["name"],
        amount=total_salary,
        month=f"{calendar.month_name[month]} {year}"
    )

    return salary_record





# from fastapi import APIRouter, Depends
# from datetime import datetime, date
# from app.database import attendance_collection, salary_collection, holiday_collection
# from app.core.auth import get_current_user
# from bson import ObjectId
# import calendar
# from tasks.send_email import send_salary_email
# router = APIRouter(tags=["salary"])

# @router.get("/calculate-salary")
# async def calculate_salary(current_user: dict = Depends(get_current_user)):
#     now = datetime.now()
#     year = now.year
#     month = now.month

#     first_day = date(year, month, 1)
#     if month == 12:
#         last_day = date(year + 1, 1, 1)
#     else:
#         last_day = date(year, month + 1, 1)

#     user_id = str(current_user["_id"])
#     total_days = calendar.monthrange(year, month)[1]
#     per_day_salary = 1000
#     total_salary = 0
#     holidays = set()
#     cursor = holiday_collection.find({
#         "date": {"$regex": f"^{year}-{month:02d}"}
#     })
#     async for h in cursor:
#         holidays.add(h["date"])

    
#     present_days = set()

#     cursor = attendance_collection.find({
#         "user_id": user_id,
#         "date": {"$gte": str(first_day), "$lt": str(last_day)}
#     })
#     async for doc in cursor:
#         date_str = doc["date"]
#         status = doc.get("status", "")
#         present_days.add(date_str)

#         if status in ("present", "cl", "short_day"):
#             total_salary += per_day_salary
#         elif status == "hdl":
#             total_salary += per_day_salary * 0.5
#         elif status in ("fdl", "lwp"):
#             total_salary += 0


#     for day in range(1, total_days + 1):
#         day_str = f"{year}-{month:02d}-{day:02d}"
#         if day_str in holidays and day_str not in present_days:
#             total_salary += per_day_salary  

    
#     salary_record = {
#         "user_id": user_id,
#         "user_name": current_user["name"],
#         "month": f"{year}-{month:02d}",
#         "total_salary": total_salary,
#         "calculated_at": datetime.utcnow()
#     }

#     existing = await salary_collection.find_one({
#         "user_id": user_id,
#         "month": f"{year}-{month:02d}"
#     })

#     if existing:
#         await salary_collection.update_one(
#             {"_id": existing["_id"]},
#             {"$set": salary_record}
#         )
#         salary_record["_id"] = str(existing["_id"])
#     else:
#         result = await salary_collection.insert_one(salary_record)
#         salary_record["_id"] = str(result.inserted_id)
    
#     return salary_record
