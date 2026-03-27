import math
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from hospitals import hospitals  # Importing your static list

app = FastAPI()

# ─── 1. THE FIX FOR "COULD NOT CONNECT" (CORS) ────────────────
# This allows your React frontend (on port 5173/3000) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmergencyRequest(BaseModel):
    lat: float
    lng: float
    type: str

# ─── 2. GEOSPATIAL ENGINE ─────────────────────────────────────
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine formula to calculate the great-circle distance 
    between two points on the Earth (in km).
    """
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.post("/api/emergency")
async def handle_emergency(request: EmergencyRequest):
    results = []
    
    # Standardize input for better matching
    requested_type = request.type.lower().strip()

    for hosp in hospitals:
        # Check if the hospital has the required specialty
        hosp_specialties = [s.lower() for s in hosp.get("specialties", [])]
        
        if requested_type in hosp_specialties or requested_type == "general":
            
            # Distance Calculation
            dist = calculate_distance(request.lat, request.lng, hosp["lat"], hosp["lng"])
            
            # --- ADVANCED SCORING LOGIC ---
            
            # A. Travel Time Score (Max 60 points)
            # Penalty: -5 points per kilometer. If > 12km, score starts dropping fast.
            time_score = max(0, 60 - (dist * 5)) 
            
            # B. Bed Availability Score (Max 40 points)
            total_beds = hosp.get("total_beds", 1)
            occupied = hosp.get("occupied_beds", 0)
            availability_ratio = (total_beds - occupied) / total_beds
            bed_score = max(0, availability_ratio * 40)
            
            # C. Rating Bonus (Max 10 points)
            # Factoring in the user rating from your data
            rating_bonus = (hosp.get("rating", 3.0) / 5) * 10
            
            final_score = round(time_score + bed_score + rating_bonus)

            results.append({
                "hospital_name": hosp["name"],
                "lat": hosp["lat"],
                "lng": hosp["lng"],
                "distance_km": round(dist, 2),
                "total_score": min(final_score, 100),
                "travel_time_score": round(time_score),
                "bed_score": round(bed_score),
                "rating": hosp.get("rating", 0)
            })

    # Sort: Highest score (best option) at the top
    sorted_results = sorted(results, key=lambda x: x["total_score"], reverse=True)

    # Return top 5 for a better map view
    return {"results": sorted_results[:5]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)