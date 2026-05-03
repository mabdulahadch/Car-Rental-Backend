from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..database import supabase
from typing import Optional
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin):
    try:
        response = supabase.table("users").select("*").eq("email", user.email).eq("password", user.password).execute()
        if not response.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    try:
        # Check if user already exists
        existing = supabase.table("users").select("id").eq("email", user.email).execute()
        if existing.data and len(existing.data) > 0:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        user_data = user.model_dump()
        # Generate a UUID for the user if the DB doesn't auto-generate one
        if "id" not in user_data or not user_data.get("id"):
            user_data["id"] = str(uuid.uuid4())
        
        response = supabase.table("users").insert(user_data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Could not create user")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
