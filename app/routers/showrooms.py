from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from ..database import supabase
from ..models import ShowroomResponse

router = APIRouter(prefix="/showrooms", tags=["showrooms"])

class ShowroomCreate(BaseModel):
    name: str
    email: str
    contact: str
    location: str
    image: Optional[List[str]] = []

class ShowroomLogin(BaseModel):
    name: str
    contact: str

@router.post("/", response_model=ShowroomResponse)
def create_showroom(showroom: ShowroomCreate):
    try:
        data = showroom.model_dump()
        response = supabase.table("showroom").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Could not create showroom")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

@router.post("/login", response_model=ShowroomResponse)
def login_showroom(credentials: ShowroomLogin):
    try:
        response = supabase.table("showroom")\
            .select("*")\
            .eq("name", credentials.name)\
            .eq("contact", credentials.contact)\
            .execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid showroom credentials"
            )
            
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {str(e)}"
        )
