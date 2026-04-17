from fastapi import APIRouter, HTTPException, status
from typing import List
from ..database import supabase
from ..models import CarCreate, CarUpdate, CarResponse, CarListResponse, CarDetailResponse

router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

@router.get("/", response_model=List[CarListResponse])
def get_available_cars():
    try:
        response = supabase.table("car").select(
            "id, brand, model, category, images, rating, location, priceperday, color, seats, fueltype"
        ).eq("isavailable", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{car_id}", response_model=CarDetailResponse)
def get_car_detail(car_id: str):
    """
    Get full car details by ID, including showroom (owner) info.
    """
    try:
        response = supabase.table("car").select(
            "*, showroom(*)"
        ).eq("id", car_id).execute()

        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/showroom/{showroom_id}", response_model=List[CarListResponse])
def get_showroom_cars(showroom_id: str):
    """
    Get all cars belonging to a specific showroom owner.
    """
    try:
        response = supabase.table("car").select(
            "id, brand, model, category, images, rating, location, priceperday, color, seats, fueltype"
        ).eq("showroomid", showroom_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def add_new_car(car: CarCreate):
    """
    2. add New Car (add new car in db)
    """
    try:
        car_data = car.model_dump(exclude_unset=True)
        response = supabase.table("car").insert(car_data).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create car")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: str):
    """
    3. delete car
    """
    try:
        response = supabase.table("car").delete().eq("id", car_id).execute()
        # In Supabase, if the row is deleted, response.data contains the deleted row(s)
        # However, checking if it was actually found depends on the returned data array length
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{car_id}", response_model=CarResponse)
def edit_car(car_id: str, car: CarUpdate):
    """
    4. edit car
    """
    try:
        car_data = car.model_dump(exclude_unset=True)
        if not car_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid fields to update")
            
        response = supabase.table("car").update(car_data).eq("id", car_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
