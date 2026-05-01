from fastapi import APIRouter, HTTPException, status
from typing import List
from ..database import supabase
from ..models import BookingCreate, BookingUpdate, BookingResponse, BookingDetailResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):
    """
    Create a new booking for a car.
    Validates that the car exists and is available before booking.
    """
    try:
        # Check if the car exists and is available
        car_check = supabase.table("car").select("id, isavailable").eq("id", booking.carid).execute()
        if not car_check.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
        if not car_check.data[0].get("isavailable", False):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Car is not available for booking")

        booking_data = booking.model_dump(exclude_unset=True)
        response = supabase.table("booking").insert(booking_data).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create booking")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[BookingResponse])
def get_all_bookings():
    """
    Get all bookings (admin/showroom use).
    """
    try:
        response = supabase.table("booking").select("*").order("createdat", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{booking_id}", response_model=BookingDetailResponse)
def get_booking_detail(booking_id: str):
    """
    Get booking details by ID including car info.
    """
    try:
        response = supabase.table("booking").select(
            "*, car(id, brand, model, category, images, rating, location, priceperday, color, seats, fueltype)"
        ).eq("id", booking_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/user/{user_id}", response_model=List[BookingDetailResponse])
def get_user_bookings(user_id: str):
    """
    Get all bookings for a specific user, including car info.
    """
    try:
        response = supabase.table("booking").select(
            "*, car(id, brand, model, category, images, rating, location, priceperday, color, seats, fueltype)"
        ).eq("userid", user_id).order("createdat", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/car/{car_id}", response_model=List[BookingResponse])
def get_car_bookings(car_id: str):
    """
    Get all bookings for a specific car (showroom owner use).
    """
    try:
        response = supabase.table("booking").select("*").eq("carid", car_id).order("createdat", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(booking_id: str, update: BookingUpdate):
    """
    Update booking status (PENDING → APPROVED / REJECTED / COMPLETED / CANCELLED).
    """
    try:
        valid_statuses = ["PENDING", "APPROVED", "REJECTED", "COMPLETED", "CANCELLED"]
        if update.status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

        response = supabase.table("booking").update(
            {"status": update.status}
        ).eq("id", booking_id).execute()

        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(booking_id: str):
    """
    Delete / cancel a booking.
    """
    try:
        response = supabase.table("booking").delete().eq("id", booking_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
