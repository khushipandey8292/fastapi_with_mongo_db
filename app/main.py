from fastapi import FastAPI
# from app.database import init_indexes
from app.router.Holidays import holidays
from app.router.Attendance import attendance
from app.router.auth import auth_routes
from app.router.Salary import salary
# from app.scheduler.schedular import start_scheduler
from app.router.User import users

app = FastAPI(title="Company API",
    version="1.0.0",
    description="API for HR operations like attendance, salary, and leaves.",
    openapi_tags=[
        {
            "name": "Auth",
            "description": "User login, registration, and token handling."
        },
        {
            "name": "Attendance",
            "description": "Mark attendance, view logs, and manage presence and apply, approve, and reject leaves"
        },
        {
            "name": "salary",
            "description": "Calculate and view salaries, deductions, and payslips."
        },
        {
            "name": "Holiday",
            "description": "Manage official company holidays."
        },
        {
           "name":"Users",
           "description":"Admin promote the users as a manager or admin."
        }
    ]
)
app.include_router(auth_routes.router)
app.include_router(users.router)
app.include_router(attendance.router)
app.include_router(salary.router)
app.include_router(holidays.router)

# @app.on_event("startup")
# async def startup():
#     await init_indexes()

# @app.on_event("startup")
# async def startup_event():
#     start_scheduler()

@app.get("/")
def home():
    return {"msg": "FastAPI with APScheduler running"}



