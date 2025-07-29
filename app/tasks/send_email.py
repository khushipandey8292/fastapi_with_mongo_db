from celery import Celery
from app.core.celery import celery_app  # import from the correct path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"))


@celery_app.task
def send_salary_email(to_email: str, name: str, amount: float, month: str):
    subject = f"Salary Slip for {month}"
    body = f"Hello {name},\n\nYour salary for {month} is ₹{amount}.\n\nRegards,\nHR Team"

    msg = MIMEMultipart()
    msg["From"] = f"{os.getenv('EMAIL_FROM_NAME')} <{os.getenv('SMTP_USER')}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        print(f"Salary email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
