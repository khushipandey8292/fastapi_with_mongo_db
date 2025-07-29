from fastapi import FastAPI
from app.router.User.users import router as newusers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(newusers)

@app.get("/promote")
def read_auth():
    return {"msg": "promotion service is working!"}
