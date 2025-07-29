from datetime import datetime, date
from app.database import attendance_collection, user_collection
from bson import ObjectId
from pytz import timezone

IST = timezone("Asia/Kolkata")

async def mark_absent_users():
    now = datetime.now(IST)
    today_str = now.strftime("%Y-%m-%d")
    readable_time = now.strftime("%d %B %Y, %I:%M %p")

    users_cursor = user_collection.find({})
    all_user_ids = [str(user["_id"]) async for user in users_cursor]

    attendance_cursor = attendance_collection.find({"date": today_str})
    marked_user_ids = set()
    async for record in attendance_cursor:
        marked_user_ids.add(record["user_id"])

    absent_user_ids = set(all_user_ids) - marked_user_ids

    for user_id in absent_user_ids:
        existing = await attendance_collection.find_one({
            "user_id": user_id,
            "date": today_str
        })
        if not existing:
            await attendance_collection.insert_one({
                "user_id": user_id,
                "status": "absent",
                "date": today_str,
                "time": readable_time,             
                "marked_at": now                  
            })

    print(f"✅ Marked {len(absent_user_ids)} users as absent for {today_str}")
