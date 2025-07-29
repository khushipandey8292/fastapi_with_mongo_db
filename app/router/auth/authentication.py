from fastapi import FastAPI
from app.router.auth.auth_routes import router as authroute
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authroute)




@app.get("/auth")
def read_auth():
    return {"msg": "Auth service is working!"}
