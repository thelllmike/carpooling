from fastapi import FastAPI
from db import engine
from app_models import user as user_models
from app_models import booking as booking_models
from app_models import trip as trip_models
from app_models import destination as destination_models
from app_models import vehicle as vehicle_models
from app_models import rating as rating_models
from routers import user as user_router
from routers import booking as booking_router
from routers import trip as trip_router
from routers import destination as destination_router
from routers import vehicle as vehicle_router
from routers import rating as rating_router
from app_models import user as user_models
from app_models import passenger as passenger_models
from app_models import notification as notification_models
from routers import user as user_router
from routers import passenger as passenger_router
from routers import notification as notification_router


# Create database tables
user_models.Base.metadata.create_all(bind=engine)
booking_models.Base.metadata.create_all(bind=engine)
trip_models.Base.metadata.create_all(bind=engine)
destination_models.Base.metadata.create_all(bind=engine)
vehicle_models.Base.metadata.create_all(bind=engine)
rating_models.Base.metadata.create_all(bind=engine)
user_models.Base.metadata.create_all(bind=engine)
passenger_models.Base.metadata.create_all(bind=engine)
notification_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])
app.include_router(trip_router.router, prefix="/trips", tags=["trips"])
app.include_router(destination_router.router, prefix="/destinations", tags=["destinations"])
app.include_router(vehicle_router.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(rating_router.router, prefix="/ratings", tags=["ratings"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(passenger_router.router, prefix="/passengers", tags=["passengers"])
app.include_router(notification_router.router, prefix="/notifications", tags=["notifications"])


@app.get("/")
def read_root():
    return {"message": "Carpooling API is running"}
