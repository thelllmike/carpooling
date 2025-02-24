import os
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from crud import user as user_crud
from schemas import user as user_schemas
from db import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
# Directory to store profile pictures
PROFILE_PIC_DIR = "profilepictures"
os.makedirs(PROFILE_PIC_DIR, exist_ok=True)


@router.put("/users/{user_id}", response_model=user_schemas.UserOut)
async def update_user_with_profile_picture(
    user_id: int,
    full_name: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    nic_number: Optional[str] = Form(None),
    license_number: Optional[str] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),  # ✅ File Upload Enabled
    db: Session = Depends(get_db),
):
    """
    Update user information and optionally upload a profile picture.
    Accepts multipart/form-data.
    """

    # Handle file upload
    pic_path = None
    if profile_picture:
        ext = profile_picture.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(PROFILE_PIC_DIR, file_name)
        with open(file_path, "wb") as buffer:
            buffer.write(await profile_picture.read())
        pic_path = file_path  # Save file path to database

    # Prepare user update data
    user_update_data = {
        "full_name": full_name,
        "password": password,
        "nic_number": nic_number,
        "license_number": license_number,
    }

    # Add profile picture only if uploaded
    if pic_path:
        user_update_data["profile_picture"] = pic_path

    # Update user in database
    updated_user = user_crud.update_user(db=db, user_id=user_id, user_update=user_update_data)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user



# Utility function to verify password
def verify_password(plain_password: str, hashed_password: str):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

# Login route
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import user as user_crud
from schemas import user as user_schemas
from db import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Utility function to verify password
def verify_password(plain_password: str, hashed_password: str):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

# Login route
@router.post("/login/")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Get user by email (username in form_data)
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    # Return required user details
    return {
        "id": user.id,
        "full_name": user.full_name,
        "is_driver": user.is_driver
    }
# Register a new user
@router.post("/users/", response_model=user_schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if a user with this email already exists
    db_user = user_crud.get_user_by_email(db, email=user.email)
    
    if db_user:
        # Check if the existing user is a driver or rider
        user_type = "Driver" if db_user.is_driver else "Rider"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email already registered with a {user_type} account."
        )

    # If email is not registered, create a new user
    return user_crud.create_user(db=db, user=user)

# Get a user by ID
@router.get("/users/{user_id}", response_model=user_schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# Delete a user by ID
@router.delete("/users/{user_id}", response_model=user_schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
# Register a new user
@router.post("/users/", response_model=user_schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

# Get a user by ID
@router.get("/users/{user_id}", response_model=user_schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update a user by ID
@router.put("/users/{user_id}", response_model=user_schemas.UserOut)
def update_user(user_id: int, user_update: user_schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete a user by ID
@router.delete("/users/{user_id}", response_model=user_schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user