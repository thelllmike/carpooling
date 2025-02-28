from typing import List
from fastapi import APIRouter, Depends, HTTPException
import joblib
import numpy as np
from sqlalchemy.orm import Session
import torch
from app_models.booking import RideBooking
from app_models.passenger import Passenger
from app_models.trip import Trip
from app_models.user import User
from app_models.vehicle import Vehicle
from crud import trip as trip_crud
from schemas import trip as trip_schemas
from db import get_db
from app_models.rating import Rating
from transformers import BartForSequenceClassification, BartTokenizer

router = APIRouter()

# ---------------------------
# Load the Trained Model
# ---------------------------
driver_model = joblib.load("models/driver_suggestion_model.pkl")
print("Driver suggestion model loaded.")

# ---------------------------
# Load BART for Sentiment Analysis
# ---------------------------
model_name = "facebook/bart-large-mnli"
tokenizer = BartTokenizer.from_pretrained(model_name)
bart_model = BartForSequenceClassification.from_pretrained(model_name, num_labels=3)

def analyze_sentiment(text: str) -> float:
    """
    Compute the sentiment score as the difference between positive and negative
    probabilities from BART, with an extra penalty for negative keywords.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = bart_model(**inputs).logits
    scores = torch.nn.functional.softmax(logits, dim=-1).tolist()[0]
    base_score = scores[2] - scores[0]
    
    # Optional extra penalty
    negative_keywords = ["poor", "bad", "subpar", "rude", "dirty", "late"]
    if any(word in text.lower() for word in negative_keywords):
        base_score -= 0.2
    return base_score

@router.get("/suggestion/", response_model=List[trip_schemas.TripDetailOut])
def get_all_trips(db: Session = Depends(get_db)):
    """
    Retrieve all trips with driver & vehicle details, then compute a predicted
    overall rating for each driver by analyzing the 'ratings' table (rating + feedback).
    Sort trips by predicted driver rating descending (drivers with no ratings last).
    """
    # 1) Query all trips with driver/vehicle details
    trips_query = (
        db.query(
            Trip,
            User.full_name,
            User.profile_picture,
            Vehicle.vehicle_type,
            Vehicle.image_link,
        )
        .join(User, Trip.user_id == User.id)
        .join(Vehicle, Trip.vehicle_id == Vehicle.id)
        .all()
    )

    if not trips_query:
        return []

    # 2) Gather all rating rows for all drivers
    all_ratings = db.query(Rating).all()
    # This yields a list of rating rows: each has .driver_id, .rating, .feedback, etc.

    # 3) Compute sentiment + overall rating for each rating row
    #    Then group them by driver_id.
    from collections import defaultdict

    driver_rows = defaultdict(list)
    for row in all_ratings:
        # If the row has no feedback, skip or set feedback to empty
        feedback_text = row.feedback or ""
        sentiment_score = analyze_sentiment(feedback_text)
        sentiment_rating = (sentiment_score + 1) * 2.5  # scale from (-1,1) to (1,5)
        
        # Combine numeric rating (0.7) + sentiment (0.3)
        # Or you can simply store them separately and feed them to the model
        # For demonstration, let's store them separately:
        driver_rows[row.driver_id].append({
            "numeric_rating": row.rating,
            "sentiment_rating": sentiment_rating
        })

    # 4) For each driver, aggregate the average numeric rating & average sentiment rating,
    #    then feed into the loaded model to get a predicted rating.
    driver_predicted_ratings = {}
    for d_id, ratings_list in driver_rows.items():
        # Average the numeric_rating
        avg_numeric_rating = np.mean([r["numeric_rating"] for r in ratings_list])
        avg_sentiment_rating = np.mean([r["sentiment_rating"] for r in ratings_list])

        # Our model expects X = [[average_rating, sentiment_rating]]
        X_features = np.array([[avg_numeric_rating, avg_sentiment_rating]])
        predicted = driver_model.predict(X_features)[0]  # single float
        driver_predicted_ratings[d_id] = predicted

    # 5) Build the response list with driver_overall_rating attached
    results = []
    for trip, full_name, profile_picture, vehicle_type, image_link in trips_query:
        driver_id = trip.user_id  # The "driver" for that trip

        # If the driver has no rating entries, we set predicted = None
        predicted_rating = driver_predicted_ratings.get(driver_id, None)

        trip_detail = trip_schemas.TripDetailOut(
            id=trip.id,
            pickup_location=trip.pickup_location,
            drop_location=trip.drop_location,
            date=trip.date,
            seats_available=trip.seats_available,
            price=trip.price,
            ride_fare=trip.ride_fare,
            estimated_time=trip.estimated_time,
            user_id=trip.user_id,
            vehicle_id=trip.vehicle_id,
            status=trip.status,
            is_completed=trip.is_completed,
            is_canceled=trip.is_canceled,
            driver_name=full_name,
            driver_profile_picture=profile_picture,
            vehicle_type=vehicle_type,
            vehicle_image=image_link,
            driver_overall_rating=predicted_rating
        )
        results.append(trip_detail)

    # 6) Sort: drivers with a rating come first (descending), None last
    #    We can do this by sorting on a tuple: (driver_overall_rating is None, -driver_overall_rating)
    #    Python sorts booleans as False < True, so "None" is sorted last.
    sorted_results = sorted(
        results,
        key=lambda x: (x.driver_overall_rating is None, -x.driver_overall_rating if x.driver_overall_rating else 0)
    )

    return sorted_results



@router.get("/trips/rider/{user_id}", response_model=List[trip_schemas.TripDetailOut])
def get_trips_by_rider(user_id: int, db: Session = Depends(get_db)):
    # Step 1: Find all Passenger records for the given rider (user)
    passenger_records = db.query(Passenger).filter(Passenger.user_id == user_id).all()
    if not passenger_records:
        raise HTTPException(status_code=404, detail="No passenger records found for this user.")
    
    # Step 2: Extract unique trip IDs from these passenger records
    trip_ids = list({record.trip_id for record in passenger_records})
    
    # Step 3: Retrieve trip details joined with driver and vehicle information
    trips_with_details = (
        db.query(
            Trip,
            User.full_name,
            User.profile_picture,
            Vehicle.vehicle_type,
            Vehicle.image_link,
        )
        .join(User, Trip.user_id == User.id)
        .join(Vehicle, Trip.vehicle_id == Vehicle.id)
        .filter(Trip.id.in_(trip_ids))
        .all()
    )
    
    if not trips_with_details:
        raise HTTPException(status_code=404, detail="No trips found for the given passenger records.")
    
    # Step 4: Map the results to the TripDetailOut schema
    results = []
    for trip, full_name, profile_picture, vehicle_type, image_link in trips_with_details:
        results.append(
            trip_schemas.TripDetailOut(
                pickup_location=trip.pickup_location,
                drop_location=trip.drop_location,
                date=trip.date,
                seats_available=trip.seats_available,
                price=trip.price,
                ride_fare=trip.ride_fare,
                estimated_time=trip.estimated_time,
                id=trip.id,
                user_id=trip.user_id,
                vehicle_id=trip.vehicle_id,
                status=trip.status,
                is_completed=trip.is_completed,
                is_canceled=trip.is_canceled,
                driver_name=full_name,
                driver_profile_picture=profile_picture,
                vehicle_type=vehicle_type,
                vehicle_image=image_link,
            )
        )
    return results

# Create a new trip
@router.post("/trips/", response_model=trip_schemas.TripOut)
def create_trip(trip: trip_schemas.TripCreate, db: Session = Depends(get_db)):
    return trip_crud.create_trip(db, trip)

# Get a trip by ID
@router.get("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def read_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = trip_crud.get_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Get trips by driver ID
@router.get("/trips/driver/{user_id}", response_model=list[trip_schemas.TripOut])
def get_trips_by_driver(user_id: int, db: Session = Depends(get_db)):
    return trip_crud.get_trips_by_driver(db, user_id)

# Update a trip
@router.put("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def update_trip(trip_id: int, trip_update: trip_schemas.TripUpdate, db: Session = Depends(get_db)):
    db_trip = trip_crud.update_trip(db, trip_id, trip_update)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Delete a trip
@router.delete("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = trip_crud.delete_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip


@router.get("/trips/", response_model=list[trip_schemas.TripDetailOut])
def get_all_trips(db: Session = Depends(get_db)):
    trips = trip_crud.get_all_trips(db)
    return trips

@router.put("/trips/seats/{trip_id}", response_model=trip_schemas.TripOut)
def update_trip_seats(trip_id: int, seat_update: trip_schemas.TripSeatUpdate, db: Session = Depends(get_db)):
    db_trip = trip_crud.update_seat_availability(db, trip_id, seat_update.seats_available)
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

