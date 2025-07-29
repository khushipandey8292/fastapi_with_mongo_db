from fastapi import FastAPI,APIRouter
from app.router.Holidays.holidays import router as newholiday
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()
app.include_router(newholiday)

@app.get("/holiday")
def read_auth():
    return {"msg": "holiday service is working!"}
