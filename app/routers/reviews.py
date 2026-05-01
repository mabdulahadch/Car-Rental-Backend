from fastapi import APIRouter, HTTPException, status
from typing import List
from ..database import supabase
from ..models import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate):
    """
    Create a new review for a car.
    After creation, recalculates the car's average rating.
    """
    try:
        review_data = review.model_dump(exclude_unset=True)
        response = supabase.table("review").insert(review_data).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create review")

        # Recalculate average rating for the car
        _update_car_rating(review.carid)

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/car/{car_id}", response_model=List[ReviewResponse])
def get_car_reviews(car_id: str):
    """
    Get all reviews for a specific car, newest first.
    """
    try:
        response = supabase.table("review").select("*").eq(
            "carid", car_id
        ).order("createdat", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: str):
    """
    Delete a review and recalculate the car's average rating.
    """
    try:
        # Get the review first so we know which car to recalculate
        review_resp = supabase.table("review").select("carid").eq("id", review_id).execute()
        if not review_resp.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        car_id = review_resp.data[0]["carid"]

        supabase.table("review").delete().eq("id", review_id).execute()

        # Recalculate average rating
        _update_car_rating(car_id)

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def _update_car_rating(car_id: str):
    """
    Helper: recalculate average rating and review count for a car.
    """
    try:
        reviews = supabase.table("review").select("rating").eq("carid", car_id).execute()
        if reviews.data:
            total = sum(r["rating"] for r in reviews.data)
            count = len(reviews.data)
            avg = round(total / count, 1)
        else:
            avg = 5.0
            count = 0

        supabase.table("car").update({
            "rating": avg,
            "reviewcount": count
        }).eq("id", car_id).execute()
    except Exception:
        pass  # Non-critical: rating update failure shouldn't crash the request
