# Carpooling Backend

The **Carpooling Backend** is a FastAPI-based project designed to support a carpooling service. It provides RESTful APIs for managing users, bookings, trips, vehicles, ratings, notifications, passengers, and other related entities. This backend serves as the foundation for carpooling applications, managing drivers, passengers, and their trips efficiently.

## Features

- User management (riders and drivers)
- Trip creation and booking system
- Vehicle and driver registration
- Passenger tracking for each trip
- Rating system for trips and passengers
- Notifications system for users
- Profile update tracking

## Technologies

- **Python 3.9+**
- **FastAPI** - Web framework for creating APIs
- **SQLAlchemy** - ORM for database management
- **Pydantic** - Data validation and parsing
- **MySQL** (or any relational database supported by SQLAlchemy)

## Project Structure


carpooling_backend/ ├── app_models/ │ ├── user.py │ ├── booking.py │ ├── trip.py │ ├── vehicle.py │ ├── destination.py │ ├── rating.py │ ├── passenger.py │ ├── notification.py │ └── profile_update.py ├── routers/ │ ├── user.py │ ├── booking.py │ ├── trip.py │ ├── vehicle.py │ ├── destination.py │ ├── rating.py │ ├── passenger.py │ ├── notification.py │ └── profile_update.py ├── schemas/ │ ├── user.py │ ├── booking.py │ ├── trip.py │ ├── vehicle.py │ ├── destination.py │ ├── rating.py │ ├── passenger.py │ ├── notification.py │ └── profile_update.py ├── crud/ │ ├── user.py │ ├── booking.py │ ├── trip.py │ ├── vehicle.py │ ├── destination.py │ ├── rating.py │ ├── passenger.py │ ├── notification.py │ └── profile_update.py ├── db.py ├── main.py └── README.md


## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/thelllmike/carpooling.git
   cd carpooling_backend


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


pip install -r requirements.txt

run 

uvicorn main:app --reload
