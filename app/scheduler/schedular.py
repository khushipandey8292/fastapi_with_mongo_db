from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from scheduler.mark_absent import mark_absent_users
from pytz import timezone

def start_scheduler():
    scheduler = AsyncIOScheduler(timezone=timezone("Asia/Kolkata"))
    scheduler.add_job(mark_absent_users, CronTrigger(hour=13, minute=5), id="mark_absent_job")
    scheduler.start()
    print("✅ APScheduler started with mark_absent_users job (IST)")
