from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import uuid
from .models import Base, Festival, User, SavedFestival, Itinerary, ItineraryFestival

# Database Configuration
DATABASE_URL = "postgresql://aiagent:aiagent@localhost/festaguide"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Festa Guide API", docs_url="/docs", redoc_url="/redoc")

# Schemas
from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID

class FestivalBase(BaseModel):
    name_en: str
    name_local: Optional[str] = None
    country_code: str
    city: Optional[str] = None
    category: Optional[str] = None
    vibe: Optional[str] = None
    start_date: date
    end_date: date
    official_url: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    verification_status: str = "pending"

class FestivalCreate(FestivalBase):
    pass

class FestivalResponse(FestivalBase):
    id: UUID
    last_updated: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password_hash: str
    preferences: Optional[dict] = None

class UserResponse(BaseModel):
    id: UUID
    email: str
    preferences: Optional[dict] = None

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Global Festival Portal API is ONLINE", "status": "running"}

@app.get("/api/v1/festivals", response_model=List[FestivalResponse])
async def get_festivals(
    category: Optional[str] = None, 
    vibe: Optional[str] = None, 
    country: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(Festival)
    if category:
        query = query.filter(Festival.category == category)
    if vibe:
        query = query.filter(Festival.vibe == vibe)
    if country:
        query = query.filter(Festival.country_code == country)
    return query.all()

@app.get("/api/v1/festivals/{festival_id}", response_model=FestivalResponse)
async def get_festival(festival_id: UUID, db: Session = Depends(get_db)):
    festival = db.query(Festival).filter(Festival.id == festival_id).first()
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")
    return festival

@app.post("/api/v1/festivals", response_model=FestivalResponse)
async def create_festival(festival: FestivalCreate, db: Session = Depends(get_db)):
    db_festival = Festival(**festival.dict())
    db.add(db_festival)
    db.commit()
    db.refresh(db_festival)
    return db_festival

@app.get("/api/v1/users/me", response_model=UserResponse)
async def get_user_me(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/v1/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/v1/festivals/{festival_id}/save", response_model=dict)
async def save_festival(festival_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    saved = SavedFestival(user_id=user_id, festival_id=festival_id)
    db.add(saved)
    db.commit()
    return {"message": "Festival saved successfully"}

@app.post("/api/v1/itineraries", response_model=dict)
async def create_itinerary(title: str, creator_id: UUID, db: Session = Depends(get_db)):
    itinerary = Itinerary(title=title, creator_id=creator_id)
    db.add(itinerary)
    db.commit()
    return {"id": itinerary.id, "message": "Itinerary created"}

@app.post("/api/v1/itineraries/{itinerary_id}/add", response_model=dict)
async def add_festival_to_itinerary(itinerary_id: UUID, festival_id: UUID, visit_order: int, db: Session = Depends(get_db)):
    item = ItineraryFestival(itinerary_id=itinerary_id, festival_id=festival_id, visit_order=visit_order)
    db.add(item)
    db.commit()
    return {"message": "Festival added to itinerary"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
