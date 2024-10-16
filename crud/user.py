from sqlalchemy.orm import Session
from app_models.user import User
from schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility function to hash passwords
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Create new user
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        is_driver=user.is_driver,
        nic_number=user.nic_number,
        license_number=user.license_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update user
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        if user_update.full_name:
            db_user.full_name = user_update.full_name
        if user_update.password:
            db_user.password = get_password_hash(user_update.password)
        if user_update.nic_number:
            db_user.nic_number = user_update.nic_number
        if user_update.license_number:
            db_user.license_number = user_update.license_number
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete user
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
