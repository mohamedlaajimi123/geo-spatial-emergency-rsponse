import math
from hospitals import get_all_hospitals
from kdtree import find_nearest_hospitals, build_kdtree, search_kdtree, haversine_distance

# ─────────────────────────────────────────────
#  HELPER — LINEAR SEARCH (brute force)
#  We use this to VERIFY the KD-Tree gives
#  the same answer as checking every hospital
# ─────────────────────────────────────────────

def linear_search(emergency_lat, emergency_lng, k=5):
    """Check every single hospital and return K closest. Slow but always correct."""
    hospitals = get_all_hospitals()
    distances = []
    for h in hospitals:
        dist = haversine_distance(emergency_lat, emergency_lng, h["lat"], h["lng"])
        distances.append((dist, h))
    distances.sort(key=lambda x: x[0])
    return distances[:k]


# ─────────────────────────────────────────────
#  HELPER — TEST RUNNER
# ─────────────────────────────────────────────

passed = 0
failed = 0

def check(test_name, condition, details=""):
    global passed, failed
    if condition:
        print(f"  ✅ PASS — {test_name}")
        passed += 1
    else:
        print(f"  ❌ FAIL — {test_name}")
        if details:
            print(f"           {details}")
        failed += 1


# ─────────────────────────────────────────────
#  TEST 1 — KD-TREE MATCHES LINEAR SEARCH
#  The most important test: KD-Tree must return
#  the exact same hospitals as brute force
# ─────────────────────────────────────────────

def test_matches_linear_search():
    print("\n── TEST 1: KD-Tree matches linear search ──────────────")

    test_locations = [
        ("Central Tunis",   36.8190, 10.1658),
        ("Sfax",            34.7400, 10.7600),
        ("Sousse",          35.8333, 10.6333),
        ("Bizerte",         37.2744,  9.8739),
        ("Gabès",           33.8833, 10.0972),
        ("Kairouan",        35.6781, 10.0963),
        ("Monastir",        35.7643, 10.8113),
        ("Nabeul",          36.4561, 10.7376),
        ("Gafsa",           34.4250,  8.7842),
        ("Tataouine",       32.9296, 10.4507),
    ]

    for name, lat, lng in test_locations:
        kd_results     = find_nearest_hospitals(lat, lng, k=5)
        linear_results = linear_search(lat, lng, k=5)

        kd_names     = [h["name"] for _, h in kd_results]
        linear_names = [h["name"] for _, h in linear_results]

        check(
            f"{name} — same hospitals as linear search",
            kd_names == linear_names,
            f"KD-Tree: {kd_names}\n           Linear : {linear_names}"
        )


# ─────────────────────────────────────────────
#  TEST 2 — RESULTS ARE SORTED BY DISTANCE
#  Closest hospital must always be first
# ─────────────────────────────────────────────

def test_results_sorted():
    print("\n── TEST 2: Results are sorted closest-first ───────────")

    test_locations = [
        ("Tunis",   36.8190, 10.1658),
        ("Sfax",    34.7400, 10.7600),
        ("Sousse",  35.8333, 10.6333),
    ]

    for name, lat, lng in test_locations:
        results   = find_nearest_hospitals(lat, lng, k=5)
        distances = [dist for dist, _ in results]
        is_sorted = all(distances[i] <= distances[i+1] for i in range(len(distances)-1))
        check(
            f"{name} — distances are in ascending order",
            is_sorted,
            f"Distances: {[round(d,2) for d in distances]}"
        )


# ─────────────────────────────────────────────
#  TEST 3 — CLOSEST HOSPITAL IS ACTUALLY CLOSE
#  For each city, #1 result must be in that city
# ─────────────────────────────────────────────

def test_closest_is_nearby():
    print("\n── TEST 3: Closest hospital is actually nearby ────────")

    # (city_name, lat, lng, max_expected_distance_km)
    city_checks = [
        ("Tunis",    36.8190, 10.1658, 5.0),
        ("Sfax",     34.7400, 10.7600, 8.0),
        ("Sousse",   35.8333, 10.6333, 8.0),
        ("Bizerte",  37.2744,  9.8739, 5.0),
        ("Monastir", 35.7643, 10.8113, 5.0),
    ]

    for name, lat, lng, max_dist in city_checks:
        results      = find_nearest_hospitals(lat, lng, k=1)
        closest_dist = results[0][0]
        check(
            f"{name} — closest hospital within {max_dist} km",
            closest_dist <= max_dist,
            f"Actual closest distance: {closest_dist:.2f} km"
        )


# ─────────────────────────────────────────────
#  TEST 4 — K PARAMETER WORKS CORRECTLY
#  Asking for k=1, k=3, k=5 must return exactly
#  that many results
# ─────────────────────────────────────────────

def test_k_values():
    print("\n── TEST 4: K parameter returns correct count ──────────")

    lat, lng = 36.8190, 10.1658  # Tunis

    for k in [1, 3, 5, 10]:
        results = find_nearest_hospitals(lat, lng, k=k)
        check(
            f"k={k} returns exactly {k} hospitals",
            len(results) == k,
            f"Actually returned: {len(results)}"
        )


# ─────────────────────────────────────────────
#  TEST 5 — NO DUPLICATE HOSPITALS IN RESULTS
#  The same hospital should never appear twice
# ─────────────────────────────────────────────

def test_no_duplicates():
    print("\n── TEST 5: No duplicate hospitals in results ──────────")

    test_locations = [
        ("Tunis",  36.8190, 10.1658),
        ("Sfax",   34.7400, 10.7600),
        ("Sousse", 35.8333, 10.6333),
    ]

    for name, lat, lng in test_locations:
        results = find_nearest_hospitals(lat, lng, k=5)
        names   = [h["name"] for _, h in results]
        check(
            f"{name} — no duplicates in top 5",
            len(names) == len(set(names)),
            f"Names returned: {names}"
        )


# ─────────────────────────────────────────────
#  TEST 6 — DISTANCES ARE POSITIVE AND REALISTIC
#  No negative distances, none above 1500 km
#  (Tunisia is ~800 km tall)
# ─────────────────────────────────────────────

def test_distances_realistic():
    print("\n── TEST 6: Distances are positive and realistic ───────")

    test_locations = [
        ("Tunis",     36.8190, 10.1658),
        ("Tataouine", 32.9296, 10.4507),
        ("Tozeur",    33.9168,  8.1295),
    ]

    for name, lat, lng in test_locations:
        results = find_nearest_hospitals(lat, lng, k=5)
        for dist, h in results:
            check(
                f"{name} → {h['name']} — distance > 0 km",
                dist >= 0,
                f"Got: {dist}"
            )
            check(
                f"{name} → {h['name']} — distance < 1500 km",
                dist < 1500,
                f"Got: {dist:.2f} km (impossibly large)"
            )


# ─────────────────────────────────────────────
#  TEST 7 — TREE STRUCTURE IS VALID
#  The built tree must not be empty and must
#  have a root with left/right children
# ─────────────────────────────────────────────

def test_tree_structure():
    print("\n── TEST 7: KD-Tree structure is valid ─────────────────")

    hospitals = get_all_hospitals()
    tree      = build_kdtree(hospitals)

    check("Tree root is not None",            tree is not None)
    check("Tree has a left subtree",          tree.left is not None)
    check("Tree has a right subtree",         tree.right is not None)
    check("Root contains a valid hospital",   "name" in tree.hospital)
    check("Root hospital has lat/lng",        "lat" in tree.hospital and "lng" in tree.hospital)

    # Count total nodes in tree (should equal 50)
    def count_nodes(node):
        if node is None:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    total = count_nodes(tree)
    check(
        f"Tree contains all 50 hospitals (found {total})",
        total == len(hospitals),
        f"Expected {len(hospitals)}, got {total}"
    )


# ─────────────────────────────────────────────
#  RUN ALL TESTS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("   KD-TREE TEST SUITE")
    print("="*55)

    test_matches_linear_search()
    test_results_sorted()
    test_closest_is_nearby()
    test_k_values()
    test_no_duplicates()
    test_distances_realistic()
    test_tree_structure()

    print("\n" + "="*55)
    print(f"   RESULTS:  {passed} passed   |   {failed} failed")
    print("="*55 + "\n")

    if failed == 0:
        print("  🎉 All tests passed! Your KD-Tree is correct.\n")
    else:
        print(f"  ⚠️  Fix the {failed} failing test(s) above.\n")