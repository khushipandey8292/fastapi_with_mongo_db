from fastapi import FastAPI
from app.router.Attendance.attendance import  router as markattendence
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(markattendence)
@app.get("/atten")
def read_auth():
    return {"msg": "Atten service is working!"}
