# ============================================================
# PERSON C: HOSPITAL RANKING - MULTI-CRITERIA SCORING SYSTEM
# ============================================================

# --- WEIGHTS (must sum to 100) ---
WEIGHTS = {
    "travel_time": 0.40,       # Speed is critical in emergencies
    "bed_availability": 0.25,  # A full hospital can't admit you
    "specialty_match": 0.20,   # Wrong specialty = wrong treatment
    "rating": 0.15,            # Quality of care matters
}

# --- EMERGENCY TYPE → REQUIRED SPECIALTY MAPPINGS ---
EMERGENCY_SPECIALTIES = {
    "cardiac":  "cardiology",
    "trauma":   "trauma_center",
    "burn":     "burn_unit",
    "stroke":   "neurology",
    "general":  None,   # No specific specialty required
}

# --- INDIVIDUAL FACTOR SCORERS (each returns 0-100) ---

def score_travel_time(travel_minutes, max_minutes=60):
    """
    Lower travel time = higher score.
    At 0 min → 100, at max_minutes or beyond → 0.
    """
    if travel_minutes >= max_minutes:
        return 0
    return round((1 - travel_minutes / max_minutes) * 100, 2)


def score_bed_availability(total_beds, occupied_beds):
    """
    Higher free bed ratio = higher score.
    100% free → 100, 100% full → 0.
    """
    if total_beds == 0:
        return 0
    free_ratio = (total_beds - occupied_beds) / total_beds
    return round(free_ratio * 100, 2)


def score_specialty_match(hospital_specialties, emergency_type):
    """
    100 → has exact specialty needed
     40 → general hospital (can handle anything, not ideal)
      0 → missing required specialty
    """
    required = EMERGENCY_SPECIALTIES.get(emergency_type)

    if required is None:
        return 100  # No specific specialty needed

    if required in hospital_specialties:
        return 100
    elif "general" in hospital_specialties:
        return 40
    else:
        return 0


def score_rating(rating, max_rating=5):
    """
    Converts star rating to 0-100 scale.
    5 stars → 100, 1 star → 20.
    """
    return round((rating / max_rating) * 100, 2)


# --- MAIN SCORING FUNCTION ---

def score_hospital(hospital, emergency_type, travel_minutes):
    """
    Scores a single hospital for a given emergency.

    Parameters:
        hospital (dict): hospital data
        emergency_type (str): e.g. "cardiac", "trauma"
        travel_minutes (float): real travel time from A* (Person B)

    Returns:
        dict: individual factor scores + total score
    """
    t_score = score_travel_time(travel_minutes)
    b_score = score_bed_availability(hospital["total_beds"], hospital["occupied_beds"])
    s_score = score_specialty_match(hospital["specialties"], emergency_type)
    r_score = score_rating(hospital["rating"])

    total = round(
        WEIGHTS["travel_time"]      * t_score +
        WEIGHTS["bed_availability"] * b_score +
        WEIGHTS["specialty_match"]  * s_score +
        WEIGHTS["rating"]           * r_score,
        2
    )

    return {
        "hospital_name":     hospital["name"],
        "travel_time_score": t_score,
        "bed_score":         b_score,
        "specialty_score":   s_score,
        "rating_score":      r_score,
        "total_score":       total,
    }


# --- RANKING FUNCTION ---

def rank_hospitals(hospitals_with_times, emergency_type):
    """
    Ranks a list of hospitals for a given emergency.

    Parameters:
        hospitals_with_times (list of tuples): [(hospital_dict, travel_minutes), ...]
        emergency_type (str): e.g. "cardiac"

    Returns:
        list of score dicts sorted by total_score descending
    """
    scored = [
        score_hospital(hospital, emergency_type, travel_minutes)
        for hospital, travel_minutes in hospitals_with_times
    ]
    return sorted(scored, key=lambda x: x["total_score"], reverse=True)


# ============================================================
# TEST CASES
# ============================================================

if __name__ == "__main__":

    # Sample hospitals (from Person A's database)
    hospital_A = {
        "name": "Hospital A",
        "total_beds": 200,
        "occupied_beds": 88,    # 44% full
        "specialties": ["cardiology", "neurology"],
        "rating": 4.5,
    }

    hospital_B = {
        "name": "Hospital B",
        "total_beds": 100,
        "occupied_beds": 95,    # 95% full
        "specialties": ["general"],
        "rating": 3.5,
    }

    emergency_type = "cardiac"
    print(f"Emergency: {emergency_type.upper()}\n")
    print(f"Hospital A travel time: 8 min  (farther)")
    print(f"Hospital B travel time: 5 min  (closer)\n")

    score_A = score_hospital(hospital_A, emergency_type, travel_minutes=8)
    score_B = score_hospital(hospital_B, emergency_type, travel_minutes=5)

    for score in [score_A, score_B]:
        print(f"--- {score['hospital_name']} ---")
        print(f"  Travel Time Score : {score['travel_time_score']}")
        print(f"  Bed Availability  : {score['bed_score']}")
        print(f"  Specialty Match   : {score['specialty_score']}")
        print(f"  Rating Score      : {score['rating_score']}")
        print(f"  TOTAL SCORE       : {score['total_score']} / 100\n")

    print("=== FINAL RANKING ===")
    ranked = rank_hospitals(
        [(hospital_A, 8), (hospital_B, 5)],
        emergency_type
    )
    for i, h in enumerate(ranked, 1):
        print(f"#{i} {h['hospital_name']} → {h['total_score']} / 100")