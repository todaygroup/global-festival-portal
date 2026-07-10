from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Festival(Base):
    __tablename__ = 'festivals'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_en = Column(String(255), nullable=False)
    name_local = Column(String(255))
    country_code = Column(String(2), nullable=False)
    city = Column(String(100))
    category = Column(String(50))
    vibe = Column(String(50))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    official_url = Column(Text)
    description = Column(Text)
    # GeoAlchemy2 is usually used for GEOGRAPHY(POINT), but for standard SQLAlchemy we'll use a string or custom type
    # In a real PostGIS env, we'd use geoalchemy2.Geometry
    location = Column(String) 
    verification_status = Column(String(20), default='pending')
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class VerificationLog(Base):
    __tablename__ = 'verification_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    festival_id = Column(UUID(as_uuid=True), ForeignKey('festivals.id'))
    verified_by = Column(String(50))
    status = Column(String(20))
    evidence_text = Column(Text)
    verified_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text)
    preferences = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class SavedFestival(Base):
    __tablename__ = 'saved_festivals'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    festival_id = Column(UUID(as_uuid=True), ForeignKey('festivals.id'), primary_key=True)
    saved_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255))
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class ItineraryFestival(Base):
    __tablename__ = 'itinerary_festivals'

    itinerary_id = Column(UUID(as_uuid=True), ForeignKey('itineraries.id'), primary_key=True)
    festival_id = Column(UUID(as_uuid=True), ForeignKey('festivals.id'), primary_key=True)
    visit_order = Column(Integer)
