from pydantic import BaseModel, Field, EmailStr, ConfigDict
from bson import ObjectId
from enum import Enum
from datetime import datetime
from pytz import timezone


class Role(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    manager = "manager"
    junior = "junior"

class AttendanceStatus(str, Enum):
    present = "present"
    cl = "casual-leave(cl)"
    lwp = "leave-without-pay(lwp)"
    hdl = "Half-day-leave(HDL)"
    fdl = "Full-day-leave(FDL)"
    short_day = "short_day" 
    absent = "absent" 
    
class AttendanceIn(BaseModel):
    status: AttendanceStatus    
    
class UserInDB(BaseModel):
    # ✅ This tells Pydantic to allow unknown types like ObjectId
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    email: EmailStr
    name: str
    hashed_password: str
    role: Role


IST = timezone('Asia/Kolkata')
now_ist = datetime.now(IST)
class AttendanceInDB(BaseModel):
    user_id: str
    user_name: str
    timezone: datetime = Field(default_factory=lambda: datetime.now(IST))
    status: AttendanceStatus