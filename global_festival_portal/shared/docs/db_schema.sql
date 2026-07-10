-- Global Festival Portal Database Schema
-- Focus: Data Integrity, Source Tracking, and Verification

CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. Festivals Table (The Core)
CREATE TABLE festivals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name_en VARCHAR(255) NOT NULL,
    name_local VARCHAR(255),
    country_code CHAR(2) NOT NULL,
    city VARCHAR(100),
    category VARCHAR(50), -- Music, Art, Food, etc.
    vibe VARCHAR(50),    -- Chill, High-Energy, etc.
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    official_url TEXT,
    description TEXT,
    location GEOGRAPHY(POINT),
    verification_status VARCHAR(20) DEFAULT 'pending', -- pending, verified, rejected
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Verification Log (The Trust Engine)
CREATE TABLE verification_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    festival_id UUID REFERENCES festivals(id),
    verified_by VARCHAR(50), -- 'AI', 'Official', 'Community'
    status VARCHAR(20),      -- 'match', 'mismatch'
    evidence_text TEXT,
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. User Profiles & Interests
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT,
    preferences JSONB, -- { "genres": [], "vibes": [], "budget": "mid" }
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Saved Festivals (My List)
CREATE TABLE saved_festivals (
    user_id UUID REFERENCES users(id),
    festival_id UUID REFERENCES festivals(id),
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, festival_id)
);

-- 5. Collaborative Itineraries
CREATE TABLE itineraries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255),
    creator_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE itinerary_festivals (
    itinerary_id UUID REFERENCES itineraries(id),
    festival_id UUID REFERENCES festivals(id),
    visit_order INTEGER,
    PRIMARY KEY (itinerary_id, festival_id)
);

CREATE INDEX idx_festivals_coords ON festivals USING GIST(location);
CREATE INDEX idx_festivals_dates ON festivals(start_date, end_date);
