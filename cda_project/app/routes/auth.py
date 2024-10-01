from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.user import User, get_password_hash, verify_password
from app.db import mongodb_client

auth_router = APIRouter()

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    role: str

@auth_router.post("/register", response_model=UserOut)
async def register(user_in: UserIn):
    user_in_db = mongodb_client.db["users"].find_one({"username": user_in.username})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user_in.password)
    user = User(username=user_in.username, password_hash=hashed_password)
    mongodb_client.db["users"].insert_one(user.dict(by_alias=True))
    
    return UserOut(id=str(user.id), username=user.username, role=user.role)

@auth_router.post("/login", response_model=UserOut)
async def login(user_in: UserIn):
    user_in_db = mongodb_client.db["users"].find_one({"username": user_in.username})
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    user = User(**user_in_db)
    if not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return UserOut(id=str(user.id), username=user.username, role=user.role)
