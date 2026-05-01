from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cars, auth, showrooms, favorites, bookings, reviews

app = FastAPI(
    title="Car Rental APIs",
    description="API for Car Rental App (Android) using Supabase DB",
    version="1.0.0"
)

# CORS configuration for calling APIs from different origins (e.g. mobile apps, web frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cars.router)
app.include_router(auth.router)
app.include_router(showrooms.router)
app.include_router(favorites.router)
app.include_router(bookings.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Car Rental API. Visit /docs to see the available endpoints."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
