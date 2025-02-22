import uuid
from fastapi import APIRouter, Depends, HTTPException ,UploadFile, File, Form
from sqlalchemy.orm import Session
from crud import vehicle as vehicle_crud
from schemas import vehicle as vehicle_schemas
from db import get_db
import os
from uuid import uuid4


router = APIRouter()

# Make sure an uploads folder exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/vehicles/", response_model=vehicle_schemas.VehicleOut)
async def create_vehicle(
    make: str,
    model: str,
    license_plate: str,
    user_id: int,
    available_seat: int,
    vehicle_type: str,
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    """
    Creates a new vehicle. Optionally accepts an uploaded image file.
    
    - make, model, license_plate, user_id, available_seat, vehicle_type are all required form fields.
    - image is optional. If provided, it will be saved to the uploads/ folder.
    """

    # If an image is uploaded, save it to the uploads folder and record its path
    image_link = None
    if image:
        # Generate a unique filename so different files don’t collide
        file_ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save file to the server
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        # You may choose to store just the filename or the entire file path
        # If you plan to serve files statically, you could store just `unique_filename`
        image_link = file_path  # e.g., "uploads/xyz.png"

    # Create a Pydantic schema object
    vehicle_data = vehicle_schemas.VehicleCreate(
        make=make,
        model=model,
        license_plate=license_plate,
        user_id=user_id,
        image_link=image_link,
        available_seat=available_seat,
        vehicle_type=vehicle_type
    )

    # Pass to our CRUD function
    db_vehicle = vehicle_crud.create_vehicle(db, vehicle_data)
    return db_vehicle

@router.get("/vehicles/{vehicle_id}", response_model=vehicle_schemas.VehicleOut)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = vehicle_crud.get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


@router.delete("/vehicles/{vehicle_id}", response_model=vehicle_schemas.VehicleOut)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = vehicle_crud.delete_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.get("/vehicles/user/{user_id}", response_model=list[vehicle_schemas.VehicleOut])
def read_vehicles_by_user(user_id: int, db: Session = Depends(get_db)):
    return vehicle_crud.get_vehicles_by_user(db, user_id)
