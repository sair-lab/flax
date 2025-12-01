"""
Batch generator for random difficult logistics problems (difficultlogistics domain),
with:
  - 1-slot trucks & airplanes
  - stacking (on-ground/on/clear)
  - loc-empty constraint for ground unloading
  - locked hubs that must be unlocked by delivering key packages to switch panels

Design:
  - Per city, roads form a spanning tree (plus optional extras).
  - Locked hubs are interior nodes on a truck->goal path in the tree.
  - For each locked hub, we create a panel reachable from a truck
    WITHOUT crossing that locked hub.
  - We always add road(panel, locked_loc) and road(locked_loc, panel).
  - We always add road(truck_start, airport) and road(airport, truck_start)
    for each truck in its city.
  - Key packages are placed only at locations reachable from a truck
    WITHOUT crossing any locked hub.
  - loc-empty is true initially for locations with no package, with at least
    one reserved empty location per city.

Problems are classified into easy/medium/hard/expert based on Fast Downward runtime.
"""

import os
import re
import time
import random
import pickle as pkl
import argparse
import subprocess
import collections
from typing import Dict, List, Tuple, Optional

from my_utils.pddl_utils import _create_planner

LOGISTICS_DOMAIN_PATH = "pddl_files/domains/difficultlogistics.pddl"


# -------------------------------------------------------------------
# Utility: find path in a tree
# -------------------------------------------------------------------

def find_path_in_tree(edges: List[Tuple[str, str]], start: str, goal: str) -> Optional[List[str]]:
    """
    Find the unique simple path between start and goal in an undirected tree
    defined by edges. Returns list of nodes [start, ..., goal] or None.
    """
    adj = collections.defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    parent = {start: None}
    queue = [start]
    while queue:
        cur = queue.pop(0)
        if cur == goal:
            break
        for nxt in adj[cur]:
            if nxt not in parent:
                parent[nxt] = cur
                queue.append(nxt)

    if goal not in parent:
        return None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


# -------------------------------------------------------------------
# World generation: stacking + loc-empty + 1-slot + locked hubs
# -------------------------------------------------------------------

def generate_random_logistics_world(
    num_cities: int,
    min_locs_per_city: int,
    max_locs_per_city: int,
    min_pkgs_per_city: int,
    max_pkgs_per_city: int,
    trucks_per_city: int,
    num_airplanes: int,
    cross_city_goal_prob: float,
    road_extra_prob: float = 0.0,     # default 0; extras are simple
    air_extra_prob: float = 0.5,
    min_goal_pkgs: int = 3,
    max_goal_pkgs: int = 5,
    max_stack_height: int = 3,
    locked_per_city: int = 1,        # we cap at 1 per city for simplicity
    num_keys: int = 2,
    seed: int = None,
) -> Dict:
    """
    Generate a random logistics world compatible with the latest difficultlogistics domain.

    Key properties:
    - loc-empty: at least one empty location per city.
    - Locked hub in a city is an interior node on some truck->goal path in the spanning tree.
    - Panel is reachable from a truck without crossing the locked hub.
    - There is a road between panel and locked location (both directions).
    - There is a road between each truck start and its city airport (both directions).
    - Key packages are at locations reachable from a truck without crossing any locked hub.
    """

    if seed is not None:
        random.seed(seed)

    # ----- Cities -----
    cities = [f"city{i+1}" for i in range(num_cities)]

    # ----- Locations per city -----
    city_locs: Dict[str, List[str]] = {}
    loc_to_city: Dict[str, str] = {}

    for ci, c in enumerate(cities, start=1):
        nlocs = random.randint(min_locs_per_city, max_locs_per_city)
        locs = [f"l{ci}_{j+1}" for j in range(nlocs)]
        city_locs[c] = locs
        for l in locs:
            loc_to_city[l] = c

    all_locations: List[str] = [l for locs in city_locs.values() for l in locs]

    # ----- Reserve at least one loc-empty per city -----
    reserved_empty_by_city: Dict[str, List[str]] = {}
    for c, locs in city_locs.items():
        if not locs:
            reserved_empty_by_city[c] = []
            continue
        reserved = [random.choice(locs)]
        reserved_empty_by_city[c] = reserved

    # ----- Airports (1 per city) -----
    airports: List[str] = []
    for c, locs in city_locs.items():
        airports.append(random.choice(locs))

    # ----- Trucks per city -----
    trucks: List[str] = []
    truck_city: Dict[str, str] = {}
    for ci, c in enumerate(cities, start=1):
        for t_idx in range(trucks_per_city):
            tname = f"truck{ci}_{t_idx+1}"
            trucks.append(tname)
            truck_city[tname] = c

    # ----- Airplanes -----
    airplanes = [f"plane{i+1}" for i in range(num_airplanes)]

    # ----- Packages per city -----
    packages: List[str] = []
    pkg_city_init: Dict[str, str] = {}
    pkgs_per_city: Dict[str, List[str]] = {}

    for ci, c in enumerate(cities, start=1):
        locs = city_locs[c]
        available_for_pkgs = [l for l in locs if l not in reserved_empty_by_city[c]]
        if not available_for_pkgs:
            available_for_pkgs = locs

        pkgs_this_city = random.randint(min_pkgs_per_city, max_pkgs_per_city)
        city_pkgs: List[str] = []
        for p_idx in range(pkgs_this_city):
            pname = f"pkg{ci}_{p_idx+1}"
            packages.append(pname)
            pkg_city_init[pname] = c
            city_pkgs.append(pname)
        pkgs_per_city[c] = city_pkgs

    if not packages:
        raise ValueError("No packages generated; adjust min_pkgs_per_city / locations.")

    # ----- Assign packages to locations & stacks -----
    pkg_loc_init: Dict[str, str] = {}
    pkg_below: Dict[str, str] = {}

    for c in cities:
        locs = city_locs[c]
        if not locs:
            continue
        allowed_locs = [l for l in locs if l not in reserved_empty_by_city[c]] or locs
        city_pkgs = pkgs_per_city.get(c, [])
        if not city_pkgs:
            continue

        random.shuffle(city_pkgs)
        remaining = list(city_pkgs)

        while remaining:
            loc = random.choice(allowed_locs)
            remaining_count = len(remaining)
            stack_height = random.randint(1, min(max_stack_height, remaining_count))
            prev_pkg = None
            for _ in range(stack_height):
                p = remaining.pop()
                pkg_loc_init[p] = loc
                pkg_below[p] = prev_pkg
                prev_pkg = p

    # ----- Per-city spanning tree (roads) -----
    tree_edges_by_city: Dict[str, List[Tuple[str, str]]] = {}
    roads_set = set()

    for c, locs in city_locs.items():
        if len(locs) <= 1:
            tree_edges_by_city[c] = []
            continue
        shuffled = locs[:]
        random.shuffle(shuffled)
        edges: List[Tuple[str, str]] = []
        for i in range(len(shuffled) - 1):
            a, b = shuffled[i], shuffled[i + 1]
            edges.append((a, b))
            roads_set.add((a, b))
            roads_set.add((b, a))
        tree_edges_by_city[c] = edges

    # ----- Air-links: airports connected, sparse -----
    air_links_set = set()
    if len(airports) > 1:
        shuffled_air = airports[:]
        random.shuffle(shuffled_air)
        for i in range(len(shuffled_air) - 1):
            a, b = shuffled_air[i], shuffled_air[i + 1]
            air_links_set.add((a, b))
            air_links_set.add((b, a))
        for i in range(len(shuffled_air)):
            for j in range(i + 1, len(shuffled_air)):
                a, b = shuffled_air[i], shuffled_air[j]
                if random.random() < air_extra_prob:
                    air_links_set.add((a, b))
                    air_links_set.add((b, a))
    air_links: List[Tuple[str, str]] = list(air_links_set)

    # ----- Vehicle positions -----
    truck_loc: Dict[str, str] = {}
    for t in trucks:
        c = truck_city[t]
        truck_loc[t] = random.choice(city_locs[c])

    airplane_loc: Dict[str, str] = {}
    for pl in airplanes:
        airplane_loc[pl] = random.choice(airports)

    # ----- has_above to compute clear / blocking -----
    has_above = {p: False for p in packages}
    for child, below in pkg_below.items():
        if below is not None:
            has_above[below] = True

    bottom_with_above = [
        p for p in packages
        if pkg_below[p] is None and has_above[p]
    ]

    # ----- Goals: few, at least one blocked-bottom goal if possible -----
    if len(packages) <= min_goal_pkgs:
        num_goal_pkgs = len(packages)
    else:
        num_goal_pkgs = random.randint(min_goal_pkgs,
                                       min(max_goal_pkgs, len(packages)))

    goal_packages: List[str] = []
    if bottom_with_above:
        blocked_goal = random.choice(bottom_with_above)
        goal_packages.append(blocked_goal)

    remaining_candidates = [p for p in packages if p not in goal_packages]
    extra_needed = max(0, num_goal_pkgs - len(goal_packages))
    if extra_needed > 0:
        if len(remaining_candidates) < extra_needed:
            extra_needed = len(remaining_candidates)
        goal_packages.extend(random.sample(remaining_candidates, extra_needed))

    used_goal_locs = set()
    pkg_goal_loc: Dict[str, str] = {}

    for p in goal_packages:
        init_city = pkg_city_init[p]
        if random.random() < cross_city_goal_prob and num_cities > 1:
            other_cities = [c for c in cities if c != init_city]
            target_city = random.choice(other_cities)
        else:
            target_city = init_city

        candidate_locs = [l for l in city_locs[target_city] if l not in used_goal_locs]
        if not candidate_locs:
            candidate_locs = [l for l in all_locations if l not in used_goal_locs]
        if not candidate_locs:
            candidate_locs = all_locations[:]

        goal_loc = random.choice(candidate_locs)
        pkg_goal_loc[p] = goal_loc
        used_goal_locs.add(goal_loc)

    # ----- loc-empty: locations with no initial package (plus reserved empties) -----
    loc_with_pkg = set(pkg_loc_init.values())
    loc_empty = set()
    for c, locs in city_locs.items():
        for l in locs:
            if l not in loc_with_pkg:
                loc_empty.add(l)
        for l in reserved_empty_by_city[c]:
            loc_empty.add(l)

    # ----- Locked hubs: interior nodes on truck->goal path -----
    locked_locs: List[str] = []
    truck_start_locs = set(truck_loc.values())
    goal_locs_set = set(pkg_goal_loc.values())

    for c, locs in city_locs.items():
        edges = tree_edges_by_city[c]
        if not edges:
            continue

        trucks_in_city = [t for t in trucks if truck_city[t] == c]
        if not trucks_in_city:
            continue
        start_loc = truck_loc[trucks_in_city[0]]

        # goals in this city
        city_goals = [gl for p, gl in pkg_goal_loc.items() if loc_to_city[gl] == c]
        candidates = set()

        for gloc in city_goals:
            path = find_path_in_tree(edges, start_loc, gloc)
            if path is None or len(path) <= 2:
                continue
            for node in path[1:-1]:  # interior nodes
                if node in truck_start_locs or node in goal_locs_set:
                    continue
                candidates.add(node)

        if not candidates:
            continue

        k = min(locked_per_city, len(candidates), 1)  # cap to 1 per city
        locked_locs.extend(random.sample(list(candidates), k))

    locked_locs = list(set(locked_locs))

    # ----- Extra roads (optional), but avoid bypass of locked hubs -----
    if road_extra_prob > 0.0:
        for c, locs in city_locs.items():
            edges = tree_edges_by_city[c]
            city_locked = [l for l in locked_locs if loc_to_city[l] == c]
            for i in range(len(locs)):
                for j in range(i + 1, len(locs)):
                    if random.random() >= road_extra_prob:
                        continue
                    a, b = locs[i], locs[j]
                    path = find_path_in_tree(edges, a, b)
                    if path is None:
                        continue
                    if any(node in city_locked for node in path):
                        continue
                    roads_set.add((a, b))
                    roads_set.add((b, a))

    # start from spanning tree + extras
    roads_set_final = set(roads_set)

    # ----- Panels & switches -----
    switch_pairs: List[Tuple[str, str]] = []  # (panel, locked_loc)

    for locked_loc in locked_locs:
        city = loc_to_city[locked_loc]
        edges = tree_edges_by_city[city]
        trucks_in_city = [t for t in trucks if truck_city[t] == city]
        if not trucks_in_city:
            continue
        start_loc = truck_loc[trucks_in_city[0]]

        candidates = []
        for l in city_locs[city]:
            if l == locked_loc:
                continue
            path = find_path_in_tree(edges, start_loc, l)
            if path is None:
                continue
            if locked_loc in path:
                continue  # panel would be behind locked hub
            candidates.append(l)

        if not candidates:
            candidates = [l for l in city_locs[city] if l != locked_loc] or city_locs[city]

        panel = random.choice(candidates)
        switch_pairs.append((panel, locked_loc))
        # ensure road between panel and locked_loc
        roads_set_final.add((panel, locked_loc))
        roads_set_final.add((locked_loc, panel))

    # ----- Ensure road between truck start and city airport -----
    for c in cities:
        city_airport = airports[cities.index(c)]
        trucks_in_city = [t for t in trucks if truck_city[t] == c]
        for t in trucks_in_city:
            start_loc = truck_loc[t]
            if start_loc != city_airport:
                roads_set_final.add((start_loc, city_airport))
                roads_set_final.add((city_airport, start_loc))

    roads: List[Tuple[str, str]] = list(roads_set_final)

    # ----- Key packages: reachable without crossing locked hubs -----
    key_candidates: List[str] = []
    locked_set = set(locked_locs)
    for p in packages:
        city = pkg_city_init[p]
        edges = tree_edges_by_city[city]
        trucks_in_city = [t for t in trucks if truck_city[t] == city]
        if not trucks_in_city:
            continue
        start_loc = truck_loc[trucks_in_city[0]]
        ploc = pkg_loc_init[p]
        path = find_path_in_tree(edges, start_loc, ploc)
        if path is None:
            continue
        if any(node in locked_set for node in path):
            continue
        key_candidates.append(p)

    max_possible_keys = min(num_keys, len(key_candidates))
    if max_possible_keys > 0:
        key_packages = random.sample(key_candidates, max_possible_keys)
    else:
        key_packages = []

    return {
        "cities": cities,
        "city_locs": city_locs,
        "airports": airports,
        "loc_to_city": loc_to_city,
        "trucks": trucks,
        "airplanes": airplanes,
        "packages": packages,
        "roads": roads,
        "air_links": air_links,
        "truck_loc": truck_loc,
        "airplane_loc": airplane_loc,
        "pkg_loc_init": pkg_loc_init,
        "pkg_city_init": pkg_city_init,
        "pkg_below": pkg_below,
        "pkg_goal_loc": pkg_goal_loc,
        "loc_empty": loc_empty,
        "locked_locs": locked_locs,
        "switch_pairs": switch_pairs,
        "key_packages": key_packages,
    }


# -------------------------------------------------------------------
# Convert world -> PDDL problem
# -------------------------------------------------------------------

def world_to_pddl(
    world: Dict,
    problem_name: str = "difficultlogistics_problem",
    domain_name: str = "difficultlogistics",
) -> str:
    """
    Convert a difficultlogistics world dict to a PDDL problem string
    for the locked-hubs + stacking + loc-empty difficultlogistics domain.
    """

    cities = world["cities"]
    city_locs = world["city_locs"]
    airports = world["airports"]
    trucks = world["trucks"]
    airplanes = world["airplanes"]
    packages = world["packages"]
    roads = world["roads"]
    air_links = world["air_links"]
    truck_loc = world["truck_loc"]
    airplane_loc = world["airplane_loc"]
    pkg_loc_init = world["pkg_loc_init"]
    pkg_below = world["pkg_below"]
    pkg_goal_loc = world["pkg_goal_loc"]
    loc_empty = world["loc_empty"]
    locked_locs = world["locked_locs"]
    switch_pairs = world["switch_pairs"]
    key_packages = world["key_packages"]

    all_locations = [l for locs in city_locs.values() for l in locs]

    # has_above for clear
    has_above = {p: False for p in packages}
    for child, below in pkg_below.items():
        if below is not None:
            has_above[below] = True

    def line(s: str, indent: int = 2) -> str:
        return " " * indent + s + "\n"

    out: List[str] = []
    out.append(f"(define (problem {problem_name})\n")
    out.append(f"  (:domain {domain_name})\n")

    # Objects
    out.append("  (:objects\n")
    if packages:
        out.append(line(" ".join(packages) + " ; packages"))
    if trucks:
        out.append(line(" ".join(trucks) + " ; trucks"))
    if airplanes:
        out.append(line(" ".join(airplanes) + " ; airplanes"))
    out.append(line(" ".join(all_locations) + " ; locations"))
    out.append(line(" ".join(cities) + " ; cities"))
    out.append("  )\n")

    # Init
    out.append("  (:init\n")

    # Type-like
    for p in packages:
        out.append(line(f"(OBJ {p})"))
    for t in trucks:
        out.append(line(f"(TRUCK {t})"))
    for pl in airplanes:
        out.append(line(f"(AIRPLANE {pl})"))
    for l in all_locations:
        out.append(line(f"(LOCATION {l})"))
    for c in cities:
        out.append(line(f"(CITY {c})"))
    for ap in airports:
        out.append(line(f"(AIRPORT {ap})"))

    # key-package
    for p in key_packages:
        out.append(line(f"(key-package {p})"))

    # loc-empty
    for l in all_locations:
        if l in loc_empty:
            out.append(line(f"(loc-empty {l})"))

    # locked locations
    for l in locked_locs:
        out.append(line(f"(locked {l})"))

    # switch-for
    for panel, loc in switch_pairs:
        out.append(line(f"(switch-for {panel} {loc})"))

    # in-city
    for c, locs in city_locs.items():
        for l in locs:
            out.append(line(f"(in-city {l} {c})"))

    # roads & air-links
    for (f, t) in roads:
        out.append(line(f"(road {f} {t})"))
    for (f, t) in air_links:
        out.append(line(f"(air-link {f} {t})"))

    # vehicle positions
    for t, l in truck_loc.items():
        out.append(line(f"(at {t} {l})"))
    for pl, l in airplane_loc.items():
        out.append(line(f"(at {pl} {l})"))

    # packages positions & stacking
    for p, loc in pkg_loc_init.items():
        out.append(line(f"(at {p} {loc})"))

    for p, below in pkg_below.items():
        if below is None:
            out.append(line(f"(on-ground {p})"))
        else:
            out.append(line(f"(on {p} {below})"))

    for p in packages:
        if not has_above[p]:
            out.append(line(f"(clear {p})"))

    # vehicle capacities
    for v in trucks + airplanes:
        out.append(line(f"(slot-free {v})"))

    out.append("  )\n")

    # Goal
    out.append("  (:goal\n")
    out.append("    (and\n")
    for p, gl in pkg_goal_loc.items():
        out.append(line(f"(at {p} {gl})", indent=6))
    out.append("    )\n")
    out.append("  )\n")
    out.append(")\n")

    return "".join(out)


# -------------------------------------------------------------------
# Difficulty helpers
# -------------------------------------------------------------------

def get_timeout_config(total_locations: int) -> Dict[str, float]:
    if total_locations <= 20:
        return {"min": 0.05, "easy": 1.0, "medium": 3.0, "hard": 8.0, "expert": 30.0}
    elif total_locations <= 40:
        return {"min": 0.1, "easy": 2.0, "medium": 6.0, "hard": 15.0, "expert": 60.0}
    elif total_locations <= 80:
        return {"min": 0.2, "easy": 4.0, "medium": 12.0, "hard": 30.0, "expert": 120.0}
    else:
        return {"min": 0.5, "easy": 10.0, "medium": 30.0, "hard": 90.0, "expert": 300.0}


def classify_difficulty(time_cost: float, timeout_cfg: Dict[str, float]) -> str:
    if timeout_cfg["min"] <= time_cost < timeout_cfg["easy"]:
        return "easy"
    if timeout_cfg["easy"] <= time_cost < timeout_cfg["medium"]:
        return "medium"
    if timeout_cfg["medium"] <= time_cost < timeout_cfg["hard"]:
        return "hard"
    if timeout_cfg["hard"] <= time_cost < timeout_cfg["expert"]:
        return "expert"
    return None


# -------------------------------------------------------------------
# Main batch generation loop
# -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Batch random difficultlogistics problem generator "
                    "(1-slot, stacking, loc-empty, locked hubs)."
    )

    parser.add_argument("--domain-file", type=str,
                        default=LOGISTICS_DOMAIN_PATH,
                        help="Path to difficultlogistics PDDL domain.")
    parser.add_argument("--root-dir", type=str,
                        default="pddl_files/problems/difficultlogistics_problems",
                        help="Root directory to store generated problems.")
    parser.add_argument("--max-per-mode", type=int, default=200,
                        help="Max number of problems per difficulty mode.")

    # World size/config
    parser.add_argument("--num-cities", type=int, default=5)
    parser.add_argument("--min-locs-per-city", type=int, default=8)
    parser.add_argument("--max-locs-per-city", type=int, default=12)
    parser.add_argument("--min-pkgs-per-city", type=int, default=6)
    parser.add_argument("--max-pkgs-per-city", type=int, default=10)
    parser.add_argument("--trucks-per-city", type=int, default=1)
    parser.add_argument("--num-airplanes", type=int, default=2)
    parser.add_argument("--cross-city-goal-prob", type=float, default=0.3)

    # parser.add_argument("--num-cities", type=int, default=2)
    # parser.add_argument("--min-locs-per-city", type=int, default=3)
    # parser.add_argument("--max-locs-per-city", type=int, default=5)
    # parser.add_argument("--min-pkgs-per-city", type=int, default=2)
    # parser.add_argument("--max-pkgs-per-city", type=int, default=4)
    # parser.add_argument("--trucks-per-city", type=int, default=1)
    # parser.add_argument("--num-airplanes", type=int, default=2)
    # parser.add_argument("--cross-city-goal-prob", type=float, default=0.3)

    # Connectivity controls
    parser.add_argument("--road-extra-prob", type=float, default=0.0,
                        help="Extra road edge prob; edges that bypass locked hubs are forbidden.")
    parser.add_argument("--air-extra-prob", type=float, default=0.5)

    # Goals
    parser.add_argument("--min-goal-pkgs", type=int, default=3)
    parser.add_argument("--max-goal-pkgs", type=int, default=5)

    # Stacking
    parser.add_argument("--max-stack-height", type=int, default=3)

    # Locks & keys
    parser.add_argument("--locked-per-city", type=int, default=2,
                        help="Max locked hubs per city (currently capped at 2).")
    parser.add_argument("--num-keys", type=int, default=2,
                        help="Number of key-packages in the world.")

    # # Goals
    # parser.add_argument("--min-goal-pkgs", type=int, default=1)
    # parser.add_argument("--max-goal-pkgs", type=int, default=2)

    # # Stacking
    # parser.add_argument("--max-stack-height", type=int, default=2)

    # # Locks & keys
    # parser.add_argument("--locked-per-city", type=int, default=1,
    #                     help="Max locked hubs per city (currently capped at 2).")
    # parser.add_argument("--num-keys", type=int, default=2,
    #                     help="Number of key-packages in the world.")

    # Misc
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--planner-name", type=str, default="fd-lama-first")
    parser.add_argument("--domain-name", type=str, default="difficultlogistics")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    modes = ["easy", "medium", "hard", "expert"]
    problem_idx = {m: 0 for m in modes}
    problem_dir = {m: {} for m in modes}

    approx_total_locations = args.num_cities * (
        (args.min_locs_per_city + args.max_locs_per_city) // 2
    )
    size_tag = f"L{approx_total_locations}"

    for mode in modes:
        problem_dir[mode]["pddl"] = os.path.join(
            args.root_dir, f"pddl_{size_tag}_{mode}"
        )
        problem_dir[mode]["world"] = os.path.join(
            args.root_dir, f"world_{size_tag}_{mode}"
        )
        problem_dir[mode]["solution"] = os.path.join(
            args.root_dir, f"solution_{size_tag}_{mode}"
        )
        for path in problem_dir[mode].values():
            os.makedirs(path, exist_ok=True)

    pddl_planner = _create_planner(args.planner_name)

    while True:
        try:
            world = generate_random_logistics_world(
                num_cities=args.num_cities,
                min_locs_per_city=args.min_locs_per_city,
                max_locs_per_city=args.max_locs_per_city,
                min_pkgs_per_city=args.min_pkgs_per_city,
                max_pkgs_per_city=args.max_pkgs_per_city,
                trucks_per_city=args.trucks_per_city,
                num_airplanes=args.num_airplanes,
                cross_city_goal_prob=args.cross_city_goal_prob,
                road_extra_prob=args.road_extra_prob,
                air_extra_prob=args.air_extra_prob,
                min_goal_pkgs=args.min_goal_pkgs,
                max_goal_pkgs=args.max_goal_pkgs,
                max_stack_height=args.max_stack_height,
                locked_per_city=args.locked_per_city,
                num_keys=args.num_keys,
                seed=None,
            )
        except ValueError as e:
            print(f"Failed to generate world: {e}")
            continue

        # Debug stats
        print("---- world stats ----")
        for k, v in world.items():
            try:
                print(f"{k}: {len(v)}")
            except TypeError:
                print(f"{k}: {v}")

        tmp_problem_path = os.path.join(
            args.root_dir, "tmp_difficultlogistics_problem.pddl"
        )
        pddl_str = world_to_pddl(
            world=world,
            problem_name="difficultlogistics_problem",
            domain_name=args.domain_name,
        )

        with open(tmp_problem_path, "w") as f:
            f.write(pddl_str)

        total_locations = sum(len(l) for l in world["city_locs"].values())
        timeout_cfg = get_timeout_config(total_locations)

        cmd_str = pddl_planner._get_cmd_str(
            args.domain_file,
            tmp_problem_path,
            timeout=timeout_cfg["expert"],
        )

        start_time = time.time()
        output = subprocess.getoutput(cmd_str)
        pddl_planner._cleanup()
        time_cost = time.time() - start_time

        if os.path.exists(tmp_problem_path):
            os.remove(tmp_problem_path)

        if "Solution found!" not in output:
            print(f"No plan found (or timeout). Time {time_cost:.2f}s.")
            continue

        fd_plan = re.findall(r"(.+) \(\d+?\)", output.lower())

        # Minimal plan length based on number of goals (not total packages)
        num_goals = len(world["pkg_goal_loc"])
        min_plan_length = max(5, num_goals * 5)

        if not fd_plan or len(fd_plan) < min_plan_length:
            print(
                f"Problem too easy or too trivial. "
                f"Time {time_cost:.2f}s, plan length {len(fd_plan)}, "
                f"min length {min_plan_length}."
            )
            continue

        mode = classify_difficulty(time_cost, timeout_cfg)
        if mode is None:
            print(
                f"Problem too hard / exceeded expert threshold. "
                f"Time {time_cost:.2f}s."
            )
            continue

        if problem_idx[mode] >= args.max_per_mode:
            print(f"Mode {mode} already has {args.max_per_mode} problems; skipping.")
            continue

        idx = problem_idx[mode]

        # Save world
        world_path = os.path.join(
            problem_dir[mode]["world"], f"difficultlogistics_world_{idx}.pkl"
        )
        with open(world_path, "wb") as f:
            pkl.dump(world, f)

        # Save PDDL
        pddl_path = os.path.join(
            problem_dir[mode]["pddl"], f"difficultlogistics_problem_{idx}.pddl"
        )
        with open(pddl_path, "w") as f:
            f.write(pddl_str)

        # Save plan
        sol_path = os.path.join(
            problem_dir[mode]["solution"], f"difficultlogistics_solution_{idx}.txt"
        )
        with open(sol_path, "w") as f:
            for move in fd_plan:
                f.write(str(move) + "\n")

        print(
            f"Found a {mode} difficultlogistics problem! "
            f"idx={idx}, time={time_cost:.2f}s, plan_len={len(fd_plan)}, "
            f"locations={total_locations}, goals={num_goals}."
        )

        problem_idx[mode] += 1


if __name__ == "__main__":
    main()
