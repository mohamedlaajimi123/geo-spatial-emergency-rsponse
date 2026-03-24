# ============================================================
# PERSON C: TEST CASES - ALL EMERGENCY TYPES
# ============================================================
# Run this file to verify the scoring system works correctly.
# Import the scoring functions from scoring_system.py
# ============================================================

from scoring_system import score_hospital, rank_hospitals

# ============================================================
# HOSPITAL DATABASE (subset from Person A)
# ============================================================

hospitals = [
    {
        "name": "Charles Nicolle Hospital",
        "total_beds": 400,
        "occupied_beds": 176,   # 44% full
        "specialties": ["cardiology", "neurology", "trauma_center"],
        "rating": 4.5,
    },
    {
        "name": "Habib Thameur Hospital",
        "total_beds": 200,
        "occupied_beds": 190,   # 95% full
        "specialties": ["general"],
        "rating": 3.5,
    },
    {
        "name": "Sahloul Hospital",
        "total_beds": 300,
        "occupied_beds": 120,   # 40% full
        "specialties": ["burn_unit", "trauma_center", "cardiology"],
        "rating": 4.2,
    },
    {
        "name": "Mongi Slim Hospital",
        "total_beds": 150,
        "occupied_beds": 60,    # 40% full
        "specialties": ["neurology", "cardiology"],
        "rating": 4.0,
    },
    {
        "name": "Regional Hospital Sfax",
        "total_beds": 250,
        "occupied_beds": 200,   # 80% full
        "specialties": ["general", "trauma_center"],
        "rating": 3.8,
    },
]

# Travel times in minutes (as given by Person B's A* algorithm)
travel_times = [12, 5, 18, 9, 25]

hospitals_with_times = list(zip(hospitals, travel_times))


# ============================================================
# HELPER: PRINT RANKING RESULTS
# ============================================================

def print_ranking(emergency_type):
    print(f"\n{'='*55}")
    print(f"  EMERGENCY: {emergency_type.upper()}")
    print(f"{'='*55}")
    ranked = rank_hospitals(hospitals_with_times, emergency_type)
    for i, h in enumerate(ranked, 1):
        print(f"\n  #{i}  {h['hospital_name']}")
        print(f"       Travel Time Score : {h['travel_time_score']}")
        print(f"       Bed Availability  : {h['bed_score']}")
        print(f"       Specialty Match   : {h['specialty_score']}")
        print(f"       Rating Score      : {h['rating_score']}")
        print(f"       ✅ TOTAL           : {h['total_score']} / 100")


# ============================================================
# TEST CASE 1: CARDIAC EMERGENCY
# Expected: Charles Nicolle or Mongi Slim should rank high
#           (both have cardiology + decent availability)
# ============================================================
print_ranking("cardiac")

# ============================================================
# TEST CASE 2: TRAUMA EMERGENCY
# Expected: Sahloul or Charles Nicolle should rank high
#           (both have trauma_center)
# ============================================================
print_ranking("trauma")

# ============================================================
# TEST CASE 3: BURN EMERGENCY
# Expected: Sahloul should rank #1
#           (only hospital with burn_unit)
# ============================================================
print_ranking("burn")

# ============================================================
# TEST CASE 4: STROKE EMERGENCY
# Expected: Charles Nicolle or Mongi Slim should rank high
#           (both have neurology)
# ============================================================
print_ranking("stroke")

# ============================================================
# TEST CASE 5: GENERAL EMERGENCY
# Expected: ranking based purely on time + beds + rating
#           specialty match = 100 for all hospitals
# ============================================================
print_ranking("general")

# ============================================================
# TEST CASE 6: PROVE CLOSEST != BEST
# Habib Thameur is closest (5 min) but should rank LOW
# because it's 95% full and has no specialty
# ============================================================
print(f"\n{'='*55}")
print("  PROOF: CLOSEST HOSPITAL ≠ BEST HOSPITAL")
print(f"{'='*55}")
print(f"\n  Habib Thameur  → closest  (5 min travel)")
print(f"  Charles Nicolle → farther (12 min travel)\n")

cardiac_ranking = rank_hospitals(hospitals_with_times, "cardiac")
for h in cardiac_ranking:
    marker = " ← CLOSEST" if h["hospital_name"] == "Habib Thameur Hospital" else ""
    print(f"  {h['hospital_name']}: {h['total_score']} / 100{marker}")