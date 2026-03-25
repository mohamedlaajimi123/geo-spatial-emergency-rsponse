import time
import math
import random
import matplotlib.pyplot as plt
from hospitals import get_all_hospitals
from kdtree import build_kdtree, search_kdtree, haversine_distance


# ─────────────────────────────────────────────
#  LINEAR SEARCH (brute force — the slow way)
# ─────────────────────────────────────────────

def linear_search(hospitals, emergency_lat, emergency_lng, k=5):
    """Check every single hospital. Correct but slow — O(n)."""
    distances = []
    for h in hospitals:
        dist = haversine_distance(emergency_lat, emergency_lng, h["lat"], h["lng"])
        distances.append((dist, h))
    distances.sort(key=lambda x: x[0])
    return distances[:k]


# ─────────────────────────────────────────────
#  GENERATE RANDOM EMERGENCY LOCATIONS
#  inside Tunisia's bounding box
# ─────────────────────────────────────────────

def random_location():
    """Return a random GPS point somewhere in Tunisia."""
    lat = random.uniform(30.2, 37.5)
    lng = random.uniform(7.5,  11.6)
    return lat, lng


# ─────────────────────────────────────────────
#  BENCHMARK FUNCTION
# ─────────────────────────────────────────────

def benchmark(num_queries=1000):
    """
    Run num_queries emergency searches using both methods.
    Returns average time in milliseconds for each.
    """
    hospitals = get_all_hospitals()
    tree      = build_kdtree(hospitals)

    locations = [random_location() for _ in range(num_queries)]

    # ── Time linear search ──
    start = time.perf_counter()
    for lat, lng in locations:
        linear_search(hospitals, lat, lng, k=5)
    linear_total = time.perf_counter() - start
    linear_avg_ms = (linear_total / num_queries) * 1000

    # ── Time KD-Tree search ──
    start = time.perf_counter()
    for lat, lng in locations:
        search_kdtree(tree, lat, lng, k=5)
    kd_total = time.perf_counter() - start
    kd_avg_ms = (kd_total / num_queries) * 1000

    return linear_avg_ms, kd_avg_ms


# ─────────────────────────────────────────────
#  TEST AT DIFFERENT HOSPITAL COUNTS
#  Show that KD-Tree scales better as n grows
# ─────────────────────────────────────────────

def benchmark_scaling():
    """
    Benchmark both methods as we increase the number of hospitals.
    Uses copies of the 50 hospitals to simulate larger datasets.
    """
    hospitals_base = get_all_hospitals()
    sizes          = [50, 100, 200, 500, 1000]
    linear_times   = []
    kd_times       = []

    print("\n── Scaling benchmark ───────────────────────────────────")
    print(f"  {'Hospitals':>10}  {'Linear (ms)':>12}  {'KD-Tree (ms)':>13}  {'Speedup':>8}")
    print(f"  {'-'*10}  {'-'*12}  {'-'*13}  {'-'*8}")

    for size in sizes:
        # Build a dataset of `size` hospitals by repeating + shifting coords slightly
        dataset = []
        for i in range(size):
            base = hospitals_base[i % len(hospitals_base)].copy()
            # Slightly offset duplicates so coords are unique
            base["lat"] += (i // len(hospitals_base)) * 0.01
            base["lng"] += (i // len(hospitals_base)) * 0.01
            dataset.append(base)

        tree      = build_kdtree(dataset)
        locations = [random_location() for _ in range(500)]

        # Linear
        start = time.perf_counter()
        for lat, lng in locations:
            linear_search(dataset, lat, lng, k=5)
        lin_ms = ((time.perf_counter() - start) / 500) * 1000

        # KD-Tree
        start = time.perf_counter()
        for lat, lng in locations:
            search_kdtree(tree, lat, lng, k=5)
        kd_ms = ((time.perf_counter() - start) / 500) * 1000

        speedup = lin_ms / kd_ms if kd_ms > 0 else 0
        linear_times.append(lin_ms)
        kd_times.append(kd_ms)

        print(f"  {size:>10}  {lin_ms:>11.4f}  {kd_ms:>12.4f}  {speedup:>7.1f}x")

    return sizes, linear_times, kd_times


# ─────────────────────────────────────────────
#  GRAPH 1 — BAR CHART: linear vs KD-Tree
#  for the actual 50-hospital dataset
# ─────────────────────────────────────────────

def plot_bar_chart(linear_ms, kd_ms):
    speedup = linear_ms / kd_ms if kd_ms > 0 else 0

    fig, ax = plt.subplots(figsize=(7, 5))

    bars = ax.bar(
        ["Linear Search\n(brute force)", "KD-Tree Search\n(our algorithm)"],
        [linear_ms, kd_ms],
        color=["#E24B4A", "#1D9E75"],
        width=0.45,
        edgecolor="white"
    )

    # Value labels on bars
    for bar, val in zip(bars, [linear_ms, kd_ms]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.002,
            f"{val:.3f} ms",
            ha="center", va="bottom", fontsize=12, fontweight="bold"
        )

    ax.set_title(
        f"Average Search Time per Query\n"
        f"KD-Tree is {speedup:.0f}× faster than Linear Search",
        fontsize=13, fontweight="bold", pad=14
    )
    ax.set_ylabel("Time (milliseconds)", fontsize=11)
    ax.set_ylim(0, linear_ms * 1.3)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig("performance_bar.png", dpi=150)
    print("\n  ✅ Saved → performance_bar.png")
    plt.show()


# ─────────────────────────────────────────────
#  GRAPH 2 — LINE CHART: how each scales
#  as number of hospitals increases
# ─────────────────────────────────────────────

def plot_scaling_chart(sizes, linear_times, kd_times):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(sizes, linear_times, color="#E24B4A", marker="o",
            linewidth=2, markersize=7, label="Linear Search  O(n)")
    ax.plot(sizes, kd_times,     color="#1D9E75", marker="s",
            linewidth=2, markersize=7, label="KD-Tree Search  O(log n)")

    ax.set_title(
        "Search Time vs Number of Hospitals\n"
        "Linear grows fast, KD-Tree stays nearly flat",
        fontsize=13, fontweight="bold", pad=14
    )
    ax.set_xlabel("Number of hospitals in database", fontsize=11)
    ax.set_ylabel("Avg time per query (ms)", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(linestyle="--", alpha=0.4)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig("performance_scaling.png", dpi=150)
    print("  ✅ Saved → performance_scaling.png")
    plt.show()


# ─────────────────────────────────────────────
#  RUN EVERYTHING
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("   KD-TREE PERFORMANCE TEST")
    print("="*55)

    # ── Part 1: benchmark on actual 50-hospital dataset ──
    print("\n── Main benchmark (1000 queries, 50 hospitals) ─────────")
    print("  Running... please wait")
    linear_ms, kd_ms = benchmark(num_queries=1000)
    speedup = linear_ms / kd_ms if kd_ms > 0 else 0

    print(f"\n  Linear Search  : {linear_ms:.4f} ms per query")
    print(f"  KD-Tree Search : {kd_ms:.4f} ms per query")
    print(f"  Speedup        : {speedup:.1f}×  faster")

    # ── Part 2: scaling benchmark ──
    sizes, linear_times, kd_times = benchmark_scaling()

    # ── Part 3: generate graphs ──
    print("\n── Generating graphs ───────────────────────────────────")
    plot_bar_chart(linear_ms, kd_ms)
    plot_scaling_chart(sizes, linear_times, kd_times)

    print("\n" + "="*55)
    print("   SUMMARY")
    print("="*55)
    print(f"  Dataset        : 50 hospitals across Tunisia")
    print(f"  Queries tested : 1000 random emergency locations")
    print(f"  Linear Search  : {linear_ms:.4f} ms  — checks all 50 hospitals")
    print(f"  KD-Tree Search : {kd_ms:.4f} ms  — checks ~log₂(50) ≈ 6 hospitals")
    print(f"  Speedup        : {speedup:.1f}× faster")
    print(f"  Graphs saved   : performance_bar.png")
    print(f"                   performance_scaling.png")
    print("="*55 + "\n")