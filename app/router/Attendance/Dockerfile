FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8006
CMD ["uvicorn", "app.router.Attendance.atten:app", "--host", "0.0.0.0", "--port", "8006", "--reload"]