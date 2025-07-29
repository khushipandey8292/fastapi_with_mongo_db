from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

celery_app = Celery(
    "salary_tasks",
    broker=os.getenv("CELERY_BROKER_URL")
)
