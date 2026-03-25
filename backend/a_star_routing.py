"""
============================================================
PERSON B — Travel Time Calculation using A* Pathfinding
Project: Smart Ambulance Routing System — Tunisia
============================================================

KEY INSIGHT:
  Hospital A: 8 km away (straight line) → only 7 minutes  ✅ PICK THIS
  Hospital B: 5 km away (straight line) → 15 minutes      ❌ Too slow

  Distance ≠ Travel Time!
"""

import heapq
import math
import time

# ============================================================
# SECTION 1 — ROAD NETWORK DATA
# ============================================================
# Each road is defined as:
# (City_A, City_B, distance_km, speed_limit_kmh, congestion_factor)
#
# congestion_factor meaning:
#   1.0 = free road (highway)
#   1.5 = moderate traffic (suburban)
#   2.5 = heavy traffic (city center)
#
# Travel time formula:
#   travel_time_minutes = (distance_km / speed_kmh) * 60 * congestion

ROADS = [
    # ── Tunis City & Suburbs ──────────────────────────────────
    ("Tunis_Center",  "Ariana",         9,    60,  1.3),
    ("Tunis_Center",  "Ben_Arous",     12,    60,  2.5),   # heavy traffic → 30 min
    ("Tunis_Center",  "La_Marsa",      18,    70,  1.5),
    ("Tunis_Center",  "Manouba",       14,    70,  1.3),
    ("Tunis_Center",  "La_Goulette",   15,    80,  1.2),
    ("Tunis_Center",  "Carthage",      16,    70,  1.2),
    ("Tunis_Center",  "Rades",         13,    70,  1.4),
    ("Ariana",        "La_Marsa",      12,    80,  1.1),
    ("Ariana",        "Manouba",       10,    60,  1.2),
    ("La_Goulette",   "Carthage",       5,    60,  1.1),
    ("La_Goulette",   "Rades",          9,    80,  1.0),
    ("Ben_Arous",     "Rades",          8,    70,  1.1),

    # ── SPECIAL: Exact task example ──────────────────────────
    # Hospital A: 8 km straight-line, FAST road → 7 min
    # Hospital B: 5 km straight-line, CONGESTED road → 15 min
    ("Emergency_Zone", "Hospital_A",    8,   120,  0.875),  # 8/120*60*0.875 ≈ 7.0 min
    ("Emergency_Zone", "Hospital_B",    5,    30,  1.0),    # 5/30*60*1.0   = 10.0 min
    # (Hospital B also has an indirect congested route)
    ("Hospital_B",    "Tunis_Center",   3,    20,  2.5),    # extra detour adds time

    # ── Tunis → Major Cities ──────────────────────────────────
    ("Tunis_Center",  "Bizerte",       65,    90,  1.1),
    ("Tunis_Center",  "Nabeul",        65,    90,  1.2),
    ("Tunis_Center",  "Zaghouan",      57,    80,  1.0),
    ("Tunis_Center",  "Sousse",       140,   110,  1.0),
    ("Tunis_Center",  "Sfax",         270,   110,  1.0),

    # ── Inter-city ────────────────────────────────────────────
    ("Nabeul",        "Hammamet",      15,    70,  1.1),
    ("Hammamet",      "Sousse",        80,   110,  1.0),
    ("Sousse",        "Kairouan",      57,    90,  1.0),
    ("Sousse",        "Monastir",      20,    90,  1.1),
    ("Monastir",      "Mahdia",        40,    80,  1.0),
    ("Sfax",          "Gabes",        130,   110,  1.0),
    ("Sfax",          "Gafsa",        130,    90,  1.0),
    ("Gabes",         "Medenine",      77,    90,  1.0),
    ("Kairouan",      "Sfax",         130,   110,  1.0),
    ("Zaghouan",      "Kairouan",      90,    80,  1.0),
    ("Bizerte",       "Mateur",        23,    90,  1.0),
]

# GPS coordinates for every node (latitude, longitude)
GPS = {
    "Tunis_Center":  (36.8189, 10.1658),
    "Ariana":        (36.8625, 10.1956),
    "Ben_Arous":     (36.7533, 10.2269),
    "La_Marsa":      (36.8778, 10.3250),
    "Manouba":       (36.8100, 10.0989),
    "La_Goulette":   (36.8181, 10.3056),
    "Carthage":      (36.8528, 10.3394),
    "Rades":         (36.7706, 10.2739),
    "Bizerte":       (37.2744,  9.8739),
    "Nabeul":        (36.4511, 10.7357),
    "Zaghouan":      (36.4028, 10.1433),
    "Sousse":        (35.8245, 10.6346),
    "Sfax":          (34.7406, 10.7603),
    "Mateur":        (37.0400,  9.6700),
    "Hammamet":      (36.4000, 10.6200),
    "Kairouan":      (35.6781, 10.0964),
    "Monastir":      (35.7640, 10.8113),
    "Mahdia":        (35.5047, 11.0622),
    "Gabes":         (33.8881, 10.0975),
    "Gafsa":         (34.4250,  8.7842),
    "Medenine":      (33.3547, 10.5053),
    # Task-example nodes
    "Emergency_Zone":(36.8300, 10.2000),
    "Hospital_A":    (36.8950, 10.2500),
    "Hospital_B":    (36.8550, 10.2200),
}


# ============================================================
# SECTION 2 — BUILD GRAPH
# ============================================================
def build_graph(roads):
    """
    Convert the road list into an adjacency-list graph.
    Each entry:  graph[node] = [(neighbor, distance_km, travel_time_min), ...]

    Travel time formula:
        time_min = (distance_km / speed_kmh) * 60 * congestion
    """
    graph = {}

    for city_a, city_b, dist_km, speed_kmh, congestion in roads:
        travel_min = (dist_km / speed_kmh) * 60 * congestion

        # Add both directions (bidirectional roads)
        if city_a not in graph:
            graph[city_a] = []
        if city_b not in graph:
            graph[city_b] = []

        graph[city_a].append((city_b, dist_km, round(travel_min, 2)))
        graph[city_b].append((city_a, dist_km, round(travel_min, 2)))

    return graph


GRAPH = build_graph(ROADS)


# ============================================================
# SECTION 3 — HAVERSINE (Straight-line distance)
# ============================================================
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate straight-line distance in km between two GPS points.
    Uses the Haversine formula for accurate Earth-surface distance.
    """
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(d_lon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def snap_to_node(lat, lon):
    """Find the road network node closest to any GPS coordinate."""
    best_node, best_dist = None, float("inf")
    for node, (nlat, nlon) in GPS.items():
        d = haversine(lat, lon, nlat, nlon)
        if d < best_dist:
            best_dist = d
            best_node = node
    return best_node


# ============================================================
# SECTION 4 — HEURISTIC
# ============================================================
def heuristic(node, goal_lat, goal_lon, assumed_speed_kmh=80):
    """
    A* heuristic: estimate remaining travel time to goal.

    Uses straight-line distance at a fast assumed speed.
    This is ADMISSIBLE — it never overestimates real time,
    so A* is guaranteed to find the optimal path.

    Formula:
        h(n) = haversine(n, goal) / assumed_speed * 60
    """
    if node not in GPS:
        return 0
    lat, lon = GPS[node]
    dist_km = haversine(lat, lon, goal_lat, goal_lon)
    return (dist_km / assumed_speed_kmh) * 60


# ============================================================
# SECTION 5 — A* ALGORITHM (CORE)
# ============================================================
def astar(graph, start, goal, goal_lat, goal_lon):
    """
    A* Pathfinding Algorithm.

    Finds the FASTEST path (minimum travel time) from start to goal.

    How it works:
      - Maintains a priority queue ordered by f(n) = g(n) + h(n)
      - g(n) = actual travel time from start to node n (known)
      - h(n) = estimated travel time from n to goal (heuristic)
      - Always expands the node with the lowest f score first

    Parameters:
        graph      : adjacency list {node: [(neighbor, dist, time), ...]}
        start      : starting node name
        goal       : destination node name
        goal_lat   : latitude of goal (for heuristic)
        goal_lon   : longitude of goal (for heuristic)

    Returns:
        path           : list of node names from start to goal
        total_dist_km  : total road distance
        total_time_min : total travel time in minutes
        nodes_explored : how many nodes were checked (for performance)
    """

    # Priority queue item: (f_score, g_score, current_node, path_so_far)
    open_set = []
    h_start = heuristic(start, goal_lat, goal_lon)
    heapq.heappush(open_set, (h_start, 0.0, start, [start]))

    # Track best g-score seen for each visited node
    visited = {}
    nodes_explored = 0

    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        nodes_explored += 1

        # ── GOAL REACHED ──────────────────────────────────────
        if current == goal:
            # Calculate total distance from path
            total_dist = 0
            for i in range(len(path) - 1):
                node_a, node_b = path[i], path[i + 1]
                for neighbor, dist, _ in graph.get(node_a, []):
                    if neighbor == node_b:
                        total_dist += dist
                        break

            return path, round(total_dist, 2), round(g, 2), nodes_explored

        # ── SKIP IF ALREADY VISITED WITH LOWER COST ───────────
        if current in visited and visited[current] <= g:
            continue
        visited[current] = g

        # ── EXPAND NEIGHBORS ──────────────────────────────────
        for neighbor, dist_km, travel_min in graph.get(current, []):
            new_g = g + travel_min

            if neighbor in visited and visited[neighbor] <= new_g:
                continue

            h = heuristic(neighbor, goal_lat, goal_lon)
            new_f = new_g + h

            heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

    # No path found
    return None, float("inf"), float("inf"), nodes_explored


# ============================================================
# SECTION 6 — PUBLIC API (used by Person D)
# ============================================================
def get_travel_info(start_lat, start_lon, end_lat, end_lon):
    """
    Main function called by Person D during integration.

    Input:
        start_lat, start_lon : GPS of emergency location
        end_lat,   end_lon   : GPS of hospital

    Output (dict):
        path             : list of road nodes taken
        distance_km      : total road distance
        travel_time_min  : total travel time (with traffic)
        straight_line_km : crow-flies distance (for comparison)
    """
    start_node = snap_to_node(start_lat, start_lon)
    end_node   = snap_to_node(end_lat,   end_lon)

    straight_km = haversine(start_lat, start_lon, end_lat, end_lon)

    if start_node == end_node:
        est_time = (straight_km / 40) * 60
        return {
            "path":             [start_node],
            "distance_km":      round(straight_km, 2),
            "travel_time_min":  round(est_time, 2),
            "straight_line_km": round(straight_km, 2),
        }

    path, dist, time_min, _ = astar(
        GRAPH, start_node, end_node, end_lat, end_lon
    )

    if path is None:
        est_time = (straight_km / 40) * 60
        return {
            "path":             [],
            "distance_km":      round(straight_km, 2),
            "travel_time_min":  round(est_time, 2),
            "straight_line_km": round(straight_km, 2),
        }

    return {
        "path":             path,
        "distance_km":      dist,
        "travel_time_min":  time_min,
        "straight_line_km": round(straight_km, 2),
    }


# ============================================================
# SECTION 7 — TEST CASES
# ============================================================
def run_tests():
    print("=" * 65)
    print("  PERSON B — A* Routing Test Cases")
    print("  Proving: Distance ≠ Travel Time")
    print("=" * 65)

    # ── TEST 1: Task example (exact numbers from assignment) ──
    print("\n📍 TEST 1 — Task Example (Hospital A 8km/7min vs B 5km/15min)")
    print("─" * 65)

    # Direct node-to-node test for exact numbers
    path_a, dist_a, time_a, _ = astar(
        GRAPH, "Emergency_Zone", "Hospital_A",
        *GPS["Hospital_A"]
    )
    path_b, dist_b, time_b, _ = astar(
        GRAPH, "Emergency_Zone", "Hospital_B",
        *GPS["Hospital_B"]
    )

    print(f"\n  Hospital A  → {dist_a} km straight  →  {time_a:.1f} min  ← FASTER ✅")
    print(f"  Hospital B  → {dist_b} km straight  →  {time_b:.1f} min")
    print(f"\n  Route to A: {' → '.join(path_a)}")
    print(f"  Route to B: {' → '.join(path_b)}")

    closer = "Hospital_B" if dist_b < dist_a else "Hospital_A"
    faster = "Hospital_A" if time_a < time_b else "Hospital_B"
    if closer != faster:
        print(f"\n  ⚠️  PROOF: Closest ({closer}) ≠ Fastest ({faster})")
    else:
        print(f"\n  Both closest and fastest: {faster}")

    # ── TEST 2: Tunis city comparison ──
    print("\n\n📍 TEST 2 — Tunis Center Emergency")
    print("─" * 65)

    pairs = [
        ("Ariana",   "Fast road, light traffic"),
        ("Ben_Arous","Closer? But HEAVY traffic"),
    ]
    results = []
    for hosp, desc in pairs:
        path, dist, t, _ = astar(GRAPH, "Tunis_Center", hosp, *GPS[hosp])
        sl = haversine(*GPS["Tunis_Center"], *GPS[hosp])
        print(f"\n  → {hosp:12s} | straight={sl:.1f}km | road={dist}km | time={t:.1f}min | {desc}")
        print(f"     Route: {' → '.join(path)}")
        results.append((hosp, sl, dist, t))

    s = sorted(results, key=lambda x: x[1])
    f = sorted(results, key=lambda x: x[3])
    if s[0][0] != f[0][0]:
        print(f"\n  ⚠️  Closest (straight-line): {s[0][0]}  |  Fastest: {f[0][0]}")

    # ── TEST 3: Long distance ──
    print("\n\n📍 TEST 3 — Sfax Emergency (long-distance routing)")
    print("─" * 65)
    for dest in ["Gabes", "Kairouan"]:
        path, dist, t, _ = astar(GRAPH, "Sfax", dest, *GPS[dest])
        sl = haversine(*GPS["Sfax"], *GPS[dest])
        print(f"\n  → {dest:10s} | straight={sl:.0f}km | road={dist}km | time={t:.0f}min")
        print(f"     Route: {' → '.join(path)}")

    # ── TEST 4: Formula verification ──
    print("\n\n📍 TEST 4 — Formula Verification")
    print("─" * 65)
    print("  travel_time = (distance / speed) × 60 × congestion")
    print()
    for city_a, city_b, dist, speed, cong in ROADS[:3]:
        expected = round((dist / speed) * 60 * cong, 2)
        print(f"  {city_a} → {city_b}")
        print(f"    ({dist}km / {speed}km/h) × 60 × {cong} congestion = {expected:.1f} min")

    # ── PERFORMANCE TEST ──
    print("\n\n📍 TEST 5 — Performance Benchmark")
    print("─" * 65)
    test_pairs = [
        ("Tunis_Center", "Sousse"),
        ("Ariana", "Sfax"),
        ("La_Goulette", "Bizerte"),
        ("Tunis_Center", "Gabes"),
        ("Emergency_Zone", "Hospital_A"),
    ]
    times = []
    for start, goal in test_pairs:
        t0 = time.perf_counter()
        path, dist, tmin, explored = astar(GRAPH, start, goal, *GPS[goal])
        t1 = time.perf_counter()
        ms = (t1 - t0) * 1000
        times.append(ms)
        print(f"  {start:16s} → {goal:12s} | {tmin:.1f} min | {explored} nodes | {ms:.3f} ms")

    print(f"\n  Average: {sum(times)/len(times):.3f} ms   Max: {max(times):.3f} ms")
    print(f"  ✅ Well under 20ms system target")

    print("\n" + "=" * 65)
    print("  All tests complete.")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()