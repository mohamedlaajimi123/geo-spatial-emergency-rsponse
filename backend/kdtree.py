import math
from hospitals import get_all_hospitals


# ─────────────────────────────────────────────
#  DISTANCE FORMULA
# ─────────────────────────────────────────────

def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate real-world distance in km between two GPS coordinates."""
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lng / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


# ─────────────────────────────────────────────
#  KD-TREE NODE
# ─────────────────────────────────────────────

class KDNode:
    """Represents one node in the KD-Tree."""
    def __init__(self, hospital, left=None, right=None):
        self.hospital = hospital
        self.left     = left
        self.right    = right


# ─────────────────────────────────────────────
#  BUILD THE KD-TREE
# ─────────────────────────────────────────────

def build_kdtree(hospital_list, depth=0):
    """
    Recursively build a KD-Tree from a list of hospitals.
      depth even  → split by latitude
      depth odd   → split by longitude
    """
    if not hospital_list:
        return None

    axis = depth % 2  # 0 = lat, 1 = lng
    key  = "lat" if axis == 0 else "lng"

    sorted_list = sorted(hospital_list, key=lambda h: h[key])
    mid         = len(sorted_list) // 2

    return KDNode(
        hospital = sorted_list[mid],
        left     = build_kdtree(sorted_list[:mid],       depth + 1),
        right    = build_kdtree(sorted_list[mid + 1:],   depth + 1),
    )


# ─────────────────────────────────────────────
#  SEARCH — K NEAREST NEIGHBORS
# ─────────────────────────────────────────────

def search_kdtree(root, emergency_lat, emergency_lng, k=5):
    """
    Find the K nearest hospitals to an emergency location.
    Returns a sorted list of (distance_km, hospital) tuples.
    """
    best = []  # list of (distance, hospital), max length = k

    def _search(node, depth=0):
        if node is None:
            return

        dist = haversine_distance(
            emergency_lat, emergency_lng,
            node.hospital["lat"], node.hospital["lng"]
        )

        # Update best list
        best.append((dist, node.hospital))
        best.sort(key=lambda x: x[0])
        if len(best) > k:
            best.pop()

        # Decide which side to go first
        axis = depth % 2
        diff = (emergency_lat - node.hospital["lat"]
                if axis == 0
                else emergency_lng - node.hospital["lng"])

        close = node.left  if diff < 0 else node.right
        far   = node.right if diff < 0 else node.left

        _search(close, depth + 1)

        # Only visit far side if the splitting plane is within current worst distance
        worst = best[-1][0] if len(best) == k else float("inf")
        if abs(diff) < worst:
            _search(far, depth + 1)

    _search(root)
    return best


# ─────────────────────────────────────────────
#  MAIN PUBLIC FUNCTION
# ─────────────────────────────────────────────

# Build the tree once at import time (fast, done only once)
_ALL_HOSPITALS = get_all_hospitals()
_TREE          = build_kdtree(_ALL_HOSPITALS)


def find_nearest_hospitals(emergency_lat, emergency_lng, k=5):
    """
    Given an emergency GPS location, return the K nearest hospitals.
    Returns a list of (distance_km, hospital_dict) sorted by distance.
    """
    results = search_kdtree(_TREE, emergency_lat, emergency_lng, k)

    print(f"\n{'='*55}")
    print(f"  EMERGENCY AT ({emergency_lat}, {emergency_lng})")
    print(f"  Top {k} nearest hospitals")
    print(f"{'='*55}")

    for rank, (dist, h) in enumerate(results, 1):
        occupancy = (h["occupied_beds"] / h["total_beds"]) * 100
        free_beds  = h["total_beds"] - h["occupied_beds"]
        print(f"\n  #{rank}  {h['name']}")
        print(f"       Distance  : {dist:.2f} km")
        print(f"       Type      : {h['type']}")
        print(f"       Specialty : {', '.join(h['specialties'])}")
        print(f"       Occupancy : {occupancy:.0f}%  ({free_beds} free beds)")
        print(f"       Rating    : {h['rating']}/5.0")

    print(f"\n{'='*55}\n")
    return results


# ─────────────────────────────────────────────
#  TESTS  (run with: python kdtree.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":

    print("\n>>> TEST 1 — Emergency in central Tunis")
    find_nearest_hospitals(36.8190, 10.1658, k=5)

    print(">>> TEST 2 — Emergency in Sfax")
    find_nearest_hospitals(34.7400, 10.7600, k=5)

    print(">>> TEST 3 — Emergency in Sousse")
    find_nearest_hospitals(35.8333, 10.6333, k=5)

    print(">>> TEST 4 — Emergency in Bizerte")
    find_nearest_hospitals(37.2744, 9.8739, k=5)

    print(">>> TEST 5 — Emergency in Gabès")
    find_nearest_hospitals(33.8833, 10.0972, k=5)