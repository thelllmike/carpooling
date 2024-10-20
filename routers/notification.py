from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import notification as notification_crud
from schemas import notification as notification_schemas
from db import get_db

router = APIRouter()

@router.post("/notifications/", response_model=notification_schemas.NotificationOut)
def create_notification(notification: notification_schemas.NotificationCreate, db: Session = Depends(get_db)):
    return notification_crud.create_notification(db, notification)

@router.get("/notifications/{notification_id}", response_model=notification_schemas.NotificationOut)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = notification_crud.get_notification(db, notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.delete("/notifications/{notification_id}", response_model=notification_schemas.NotificationOut)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = notification_crud.delete_notification(db, notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification
