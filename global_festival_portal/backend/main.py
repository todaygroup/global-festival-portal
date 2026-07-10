from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Festa Guide API", docs_url="/docs", redoc_url="/redoc")

# Mocked Data for immediate verification of "Living" system
# In next step, this will be connected to the real DB and Scraper
MOCK_FESTIVALS = [
    {
        "id": str(uuid.uuid4()),
        "name": "Tomorrowland",
        "country": "Belgium",
        "status": "Verified",
        "vibe": "High Energy"
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Sapporo Snow Festival",
        "country": "Japan",
        "status": "Verified",
        "vibe": "Chill"
    }
]

class FestivalSchema(BaseModel):
    id: str
    name: str
    country: str
    status: str
    vibe: str

@app.get("/")
async def root():
    return {"message": "Global Festival Portal API is ONLINE", "status": "running"}

@app.get("/api/v1/festivals", response_model=List[FestivalSchema])
async def get_festivals():
    return MOCK_FESTIVALS

@app.get("/api/v1/festivals/{festival_id}")
async def get_festival(festival_id: str):
    festival = next((f for f in MOCK_FESTIVALS if f["id"] == festival_id), None)
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")
    return festival

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
