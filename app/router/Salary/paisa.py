from fastapi import FastAPI
from app.router.Salary.salary import router as salroute
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(salroute)

@app.get("/salary")
def read_auth():
    return {"msg": "salary service is working, which is very important That's why I am a good thinker. !"}
