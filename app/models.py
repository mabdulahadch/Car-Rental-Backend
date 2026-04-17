from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CarBase(BaseModel):
    brand: str
    model: str
    category: Optional[str] = None
    priceperday: float
    seats: Optional[int] = 5
    enginepower: Optional[str] = None
    maxspeed: Optional[str] = None
    fueltype: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = []
    registration: Optional[str] = None
    features: Optional[List[str]] = []
    showroomid: Optional[str] = None
    location: Optional[str] = None
    isavailable: Optional[bool] = True
    rating: Optional[float] = 5.0
    reviewcount: Optional[int] = 0

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    category: Optional[str] = None
    priceperday: Optional[float] = None
    seats: Optional[int] = None
    enginepower: Optional[str] = None
    maxspeed: Optional[str] = None
    fueltype: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    registration: Optional[str] = None
    features: Optional[List[str]] = None
    showroomid: Optional[str] = None
    location: Optional[str] = None
    isavailable: Optional[bool] = None
    rating: Optional[float] = None
    reviewcount: Optional[int] = None

class CarResponse(CarBase):
    id: str
    createdat: datetime

class CarListResponse(BaseModel):
    """Slim response for listing available cars"""
    id: str
    brand: str
    model: str
    category: Optional[str] = None
    images: Optional[List[str]] = []
    rating: Optional[float] = 5.0
    location: Optional[str] = None
    priceperday: float
    color: Optional[str] = None
    seats: Optional[int] = 5
    fueltype: Optional[str] = None

class ShowroomResponse(BaseModel):
    """Showroom / Owner details"""
    id: str
    name: str
    email: str
    contact: Optional[str] = None
    location: Optional[str] = None
    image: Optional[List[str]] = []
    createdat: Optional[datetime] = None

class CarDetailResponse(CarBase):
    """Full car details with showroom (owner) info"""
    id: str
    createdat: datetime
    showroom: Optional[ShowroomResponse] = None
