from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
from ..database import supabase

router = APIRouter(prefix="/favorites", tags=["favorites"])

class FavoriteAddRequest(BaseModel):
    user_id: str
    car_id: str

class FavoriteResponse(BaseModel):
    id: str
    user_id: str
    car_id: str

@router.post("/", response_model=FavoriteResponse)
def add_favorite(fav: FavoriteAddRequest):
    try:
        data = fav.model_dump()
        response = supabase.table("favorites").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Could not add to favorites")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

@router.delete("/{user_id}/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(user_id: str, car_id: str):
    try:
        supabase.table("favorites").delete().eq("user_id", user_id).eq("car_id", car_id).execute()
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=List[str])
def get_user_favorites(user_id: str):
    try:
        response = supabase.table("favorites").select("car_id").eq("user_id", user_id).execute()
        car_ids = [item["car_id"] for item in response.data]
        return car_ids
    except Exception as e:
        # Graceful fallback: return empty list
        return []
