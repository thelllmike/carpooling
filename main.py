from fastapi import FastAPI
from db import engine
from app_models import user as user_models
from app_models import booking as booking_models
from app_models import trip as trip_models  # Import trip model
from routers import user as user_router
from routers import booking as booking_router
from routers import trip as trip_router  # Import trip router

# Create database tables
user_models.Base.metadata.create_all(bind=engine)
booking_models.Base.metadata.create_all(bind=engine)
trip_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers with route prefixes and tags for Swagger UI documentation
app.include_router(user_router.router, prefix="/users", tags=["users"])          # All user-related routes will be under /users
app.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])  # All booking-related routes will be under /bookings
app.include_router(trip_router.router, prefix="/trips", tags=["trips"])           # All trip-related routes will be under /trips

@app.get("/")
def read_root():
    return {"message": "Carpooling API is running"}
