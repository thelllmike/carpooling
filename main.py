from fastapi import FastAPI
from db import engine
from app_models import user as models  # Updated import after renaming folder
from routers import user  # Absolute import

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the user router
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Carpooling API is running"}
