from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import everyone's work!
from kdtree import find_nearest_hospitals 
from a_star_routing import get_travel_info
from scoring_system import rank_hospitals

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmergencyRequest(BaseModel):
    lat: float
    lng: float
    type: str # e.g., "cardiac", "trauma", "general"

@app.post("/api/emergency")
def handle_emergency(req: EmergencyRequest):
    # ==========================================
    # STEP 1: PERSON A (KD-Tree)
    # ==========================================
    closest_hospitals = find_nearest_hospitals(req.lat, req.lng, k=5)
    
    # ==========================================
    # STEP 2: PERSON B (A* Routing)
    # ==========================================
    hospitals_for_scoring = []
    
    for item in closest_hospitals:
        # --- THE FIX IS HERE ---
        # If Person A returned a tuple like (distance, hospital_dict), grab the dict!
        if isinstance(item, tuple):
            # The dictionary is usually the second item (index 1), but we check both just in case
            hosp = item[1] if isinstance(item[1], dict) else item[0]
        else:
            hosp = item # Just in case it was already a dict
        # -----------------------
        
        # Now 'hosp' is guaranteed to be the dictionary!
        route_info = get_travel_info(req.lat, req.lng, hosp["lat"], hosp["lng"])
        travel_minutes = route_info["travel_time_min"]
        
        hospital_data = {
            "name": hosp.get("name", "Unknown Hospital"),
            "lat": hosp["lat"],
            "lng": hosp["lng"],
            "total_beds": hosp.get("total_beds", 200),
            "occupied_beds": hosp.get("occupied_beds", 100),
            "specialties": hosp.get("specialties", ["general", "cardiology", "trauma_center"]),
            "rating": hosp.get("rating", 4.0),
            "road_distance_km": route_info["distance_km"],
            "route_path": route_info["path"]
        }
        
        hospitals_for_scoring.append((hospital_data, travel_minutes))
        
    # ==========================================
    # STEP 3: PERSON C (Scoring & Ranking)
    # ==========================================
    ranked_results = rank_hospitals(hospitals_for_scoring, req.type)
    
    return {
        "status": "success", 
        "emergency_type": req.type,
        "results": ranked_results
    }