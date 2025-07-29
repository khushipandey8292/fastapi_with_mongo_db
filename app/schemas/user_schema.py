from pydantic import BaseModel, EmailStr
from typing import Optional
from app.model.user_model import Role, AttendanceStatus
from datetime import date,datetime

  
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: Role

class Token(BaseModel):
    access_token: str
    token_type: str

    
class AttendanceCreate(BaseModel):
    user_id: str
    date: date
    status: AttendanceStatus


class AttendancePublic(BaseModel):
    id: Optional[str]
    user_id: str
    user_name: str
    status: AttendanceStatus
    time: Optional[str] = None
   

class HolidayCreate(BaseModel):
    date: date
    reason: Optional[str] = "Holiday"

class HolidayPublic(BaseModel):
    id: str
    date: date
    reason: Optional[str]