FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 8007
CMD ["uvicorn", "app.router.Salary.paisa:app", "--host", "0.0.0.0", "--port", "8007", "--reload"]