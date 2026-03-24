# Person C: Hospital Ranking Module
## Multi-Criteria Scoring System

---

## What This Module Does

When an emergency happens, the closest hospital is not always the best choice.
This module scores and ranks hospitals based on **4 factors** to find the truly best option for each emergency type.

---

## Files

| File | Description |
|---|---|
| `scoring_system.py` | Main module — all scoring and ranking logic |
| `test_scoring.py` | Test cases for all 5 emergency types |

---

## Scoring System

Each hospital receives a score from **0 to 100** based on 4 weighted factors:

| Factor | Weight | Why |
|---|---|---|
| Travel Time | 40% | Every second counts in an emergency |
| Bed Availability | 25% | A full hospital cannot admit the patient |
| Specialty Match | 20% | Wrong specialty = wrong or delayed treatment |
| Rating | 15% | Higher-rated hospitals provide better care |

**Formula:**
```
total_score = (0.40 × time_score) + (0.25 × bed_score) + (0.20 × specialty_score) + (0.15 × rating_score)
```

---

## Emergency Type → Specialty Mapping

| Emergency | Required Specialty |
|---|---|
| cardiac | cardiology |
| trauma | trauma_center |
| burn | burn_unit |
| stroke | neurology |
| general | none (any hospital works) |

**Specialty scoring rules:**
- Hospital has required specialty → **100**
- Hospital is general (no specialty) → **40**
- Hospital is missing required specialty → **0**

---

## How to Use (for Person D)

### 1. Score a single hospital
```python
from scoring_system import score_hospital

result = score_hospital(hospital, emergency_type, travel_minutes)
```

**Input:**
```python
hospital = {
    "name": "Charles Nicolle Hospital",
    "total_beds": 400,
    "occupied_beds": 176,
    "specialties": ["cardiology", "neurology"],
    "rating": 4.5,
}
emergency_type = "cardiac"   # "cardiac", "trauma", "burn", "stroke", "general"
travel_minutes = 12          # from Person B's A* algorithm
```

**Output:**
```python
{
    "hospital_name":     "Charles Nicolle Hospital",
    "travel_time_score": 80.0,
    "bed_score":         56.0,
    "specialty_score":   100,
    "rating_score":      90.0,
    "total_score":       79.5   # out of 100
}
```

---

### 2. Rank multiple hospitals
```python
from scoring_system import rank_hospitals

ranked = rank_hospitals(hospitals_with_times, emergency_type)
```

**Input:**
```python
hospitals_with_times = [
    (hospital_A, 12),   # (hospital dict, travel time in minutes)
    (hospital_B, 5),
    (hospital_C, 18),
]
emergency_type = "cardiac"
```

**Output:** list of score dicts sorted from best (#1) to worst.

---

## Key Result: Closest ≠ Best

| Hospital | Travel Time | Beds Free | Specialty | Score |
|---|---|---|---|---|
| Mongi Slim | 9 min | 60% | ✅ cardiology | **81.0 / 100** |
| Charles Nicolle | 12 min | 56% | ✅ cardiology | 79.5 / 100 |
| Habib Thameur | **5 min (closest)** | 5% | ❌ none | 56.4 / 100 |

> Habib Thameur is the closest hospital but ranks **last** for a cardiac emergency — it's 95% full and has no cardiology unit.

---

## How to Run Tests

Make sure both files are in the same folder, then:

```bash
python test_scoring.py
```