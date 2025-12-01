import re
import subprocess
import time
import numpy as np
import random
import os
import pickle as pkl

from my_utils.pddl_utils import _create_planner

# -----------------------------
# Grid cell types
# -----------------------------
EMPTY = 0
WALL = 1
BOX = 2
ROBOT = 3
GOAL = 4   # only for visualization

# -----------------------------
# Random map generation
# -----------------------------

def generate_random_sokomindplus_map(
    size,
    wall_prob=0.2,
    min_total_boxes=6,
    max_total_boxes=12,
    min_goal_boxes=1,
    max_goal_boxes=3,
):
    """
    Generate a random Sokomind map of shape (size x size).

    - Each cell is either a wall or free, i.e. we do NOT force an outer wall ring.
    - Place one robot on a free cell.
    - Place many boxes (total_boxes).
    - Randomly choose a small subset of boxes as "goal boxes".
    - For each goal box, choose a goal position that is currently free (no box, no wall).
      Note: the goal positions may coincide with the robot's start cell or other empty cells.

    Returns:
        grid: np.array[int] with values in {EMPTY, WALL, BOX, ROBOT, GOAL}
        robot_pos: (y, x)
        box_positions: list[(y, x)] of length total_boxes
        goal_box_indices: list[int] (subset of [0..total_boxes-1] for boxes in the goal)
        goal_positions: list[(y, x)] aligned with goal_box_indices
    """

    # Start with an empty grid
    grid = np.zeros((size, size), dtype=int)

    # Randomly assign walls across the whole grid (no special outer ring)
    for y in range(size):
        for x in range(size):
            if random.random() < wall_prob:
                grid[y, x] = WALL

    # Collect free cells (non-wall) for placing robot and boxes
    empties = list(zip(*np.where(grid == EMPTY)))
    if len(empties) < 3:
        # Not enough free cells to place robot + boxes + goals
        raise ValueError("Not enough free cells to place robot and boxes.")

    # Sample robot position
    robot_pos = random.choice(empties)
    empties.remove(robot_pos)
    grid[robot_pos] = ROBOT

    # Decide total number of boxes (many of them will be irrelevant to the goal)
    total_boxes = random.randint(min_total_boxes, max_total_boxes)
    # Keep some cells for goal positions
    total_boxes = min(total_boxes, len(empties) - 1)

    if total_boxes <= 0:
        total_boxes = 1

    print(f"Generating map with {total_boxes} boxes.")

    # Place all boxes
    box_positions = random.sample(empties, total_boxes)
    for pos in box_positions:
        grid[pos] = BOX
        empties.remove(pos)

    # Decide how many boxes are goal boxes (a small subset)
    max_goal_boxes = min(max_goal_boxes, total_boxes)
    if max_goal_boxes <= 0:
        max_goal_boxes = 1
    goal_box_count = random.randint(min_goal_boxes, max_goal_boxes)

    # Choose which boxes are goal boxes
    goal_box_indices = random.sample(range(total_boxes), goal_box_count)

    # Choose goal positions for each goal box (must be free cells: no wall, no box)
    if len(empties) < goal_box_count:
        raise ValueError("Not enough free cells to place goals.")
    goal_positions = random.sample(empties, goal_box_count)
    for pos in goal_positions:
        grid[pos] = GOAL

    return grid, robot_pos, box_positions, goal_box_indices, goal_positions


# -----------------------------
# Grid -> PDDL problem
# -----------------------------

def grid_to_pddl_sokomindplus(
    size,
    grid,
    robot_pos,
    box_positions,
    goal_box_indices,
    goal_positions,
    problem_name="sokomindplus_problem",
    domain_name="sokomindplus",
    tmp_pddl_path="sokomindplus_problems/tmp_sokomindplus_problem.pddl",
):
    """
    Convert a Sokomind grid and layout into a PDDL problem instance
    for the given sokomindplus domain.

    Encoding assumptions:

    - Positions:
        p0, p1, ..., p(N-1), where index = y * size + x.
    - Robot:
        r - robot
        (rAt r p<idx>) in init.
    - Boxes:
        b0, b1, ..., b(total_boxes-1) - obj
        Each box has (isBox b<i>) and an initial (oAt b<i> p<idx>).
    - posEmpty:
        (posEmpty p<i>) holds for FREE cells that have NO BOX initially.
        Robot presence does not affect posEmpty, consistent with your domain.
    - Adjacency:
        upTo pA pB  means "pA is above pB" (A.y = B.y - 1).
        downTo pA pB means "pA is below pB".
        leftTo pA pB means "pA is left of pB".
        rightTo pA pB means "pA is right of pB".
        We only create these relations between non-wall cells.
    - Goal:
        Only the goal boxes appear in the goal:
        (:goal (and (oAt b<i0> p<gidx0>) (oAt b<i1> p<gidx1>) ... ))
    """

    assert len(goal_box_indices) == len(goal_positions)
    num_boxes = len(box_positions)

    # ---------- Objects ----------
    object_lines = []
    object_lines.append("r - robot")

    # Box objects
    for i in range(num_boxes):
        object_lines.append(f"b{i} - obj")

    # Position objects (including walls; walls just have no adjacency)
    for y in range(size):
        for x in range(size):
            idx = y * size + x
            object_lines.append(f"p{idx} - pos")

    # ---------- Init ----------
    init_lines = []

    # Robot initial position
    r_idx = robot_pos[0] * size + robot_pos[1]
    init_lines.append(f"(rAt r p{r_idx})")

    # Boxes initial positions + isBox
    box_set = set(box_positions)
    for i, (y, x) in enumerate(box_positions):
        idx = y * size + x
        init_lines.append(f"(oAt b{i} p{idx})")
        init_lines.append(f"(isBox b{i})")

    # posEmpty: all non-wall cells that do NOT contain a box
    for y in range(size):
        for x in range(size):
            if grid[y, x] == WALL:
                continue
            if (y, x) in box_set:
                continue
            idx = y * size + x
            init_lines.append(f"(posEmpty p{idx})")

    # Adjacency relations between non-wall cells
    for y in range(size):
        for x in range(size):
            if grid[y, x] == WALL:
                continue

            idx = y * size + x

            # Cell above: (y-1, x)
            if y > 0 and grid[y - 1, x] != WALL:
                up_idx = (y - 1) * size + x
                # upTo above, current
                init_lines.append(f"(upTo p{up_idx} p{idx})")
                # downTo current, above
                init_lines.append(f"(downTo p{idx} p{up_idx})")

            # Cell below: (y+1, x)
            if y < size - 1 and grid[y + 1, x] != WALL:
                down_idx = (y + 1) * size + x
                # downTo below, current
                init_lines.append(f"(downTo p{down_idx} p{idx})")
                # upTo current, below
                init_lines.append(f"(upTo p{idx} p{down_idx})")

            # Cell to the left: (y, x-1)
            if x > 0 and grid[y, x - 1] != WALL:
                left_idx = y * size + (x - 1)
                # leftTo left, current
                init_lines.append(f"(leftTo p{left_idx} p{idx})")
                # rightTo current, left
                init_lines.append(f"(rightTo p{idx} p{left_idx})")

            # Cell to the right: (y, x+1)
            if x < size - 1 and grid[y, x + 1] != WALL:
                right_idx = y * size + (x + 1)
                # rightTo right, current
                init_lines.append(f"(rightTo p{right_idx} p{idx})")
                # leftTo current, right
                init_lines.append(f"(leftTo p{idx} p{right_idx})")

    # ---------- Goal: only goal boxes ----------
    goal_lines = []
    for (box_i, (gy, gx)) in zip(goal_box_indices, goal_positions):
        g_idx = gy * size + gx
        goal_lines.append(f"(oAt b{box_i} p{g_idx})")

    objects_str = "\n        ".join(object_lines)
    init_str = "\n        ".join(init_lines)
    goal_str = "\n          ".join(goal_lines)

    pddl_str = f"""(define (problem {problem_name})
  (:domain {domain_name})
  (:objects
        {objects_str}
  )
  (:init
        {init_str}
  )
  (:goal
        (and
          {goal_str}
        )
  )
)"""

    os.makedirs(os.path.dirname(tmp_pddl_path), exist_ok=True)
    with open(tmp_pddl_path, "w") as f:
        f.write(pddl_str)

    return pddl_str


# -----------------------------
# Main loop: generate + solve + classify
# -----------------------------

if __name__ == "__main__":
    # Path to your sokomindplus domain
    pddl_domain_file_path = "pddl_files/domains/sokomindplus.pddl"
    tmp_pddl_problem_path = "tmp_sokomindplus_problem.pddl"
    MAX_PROBLEM_NUM = 200

    problem_size = 20

    # Timeouts and difficulty thresholds per size
    if problem_size == 10:
        timeout = {
            "min": 0.05,
            "easy": 1,
            "medium": 3,
            "hard": 5,
            "expert": 15,
        }
    elif problem_size == 15:
        timeout = {
            "min": 0.1,
            "easy": 2,
            "medium": 6,
            "hard": 10,
            "expert": 30,
        }
    elif problem_size == 18:
        timeout = {
            "min": 3,
            "easy": 10,
            "medium": 25,
            "hard": 40,
            "expert": 120,
        }
    else:  # default for 20
        timeout = {
            "min": 10,
            "easy": 30,
            "medium": 60,
            "hard": 120,
            "expert": 300,
        }

    # Minimal plan length filter to discard trivial instances
    min_plan_length = int(0.1 * problem_size ** 2)

    problem_idx = {
        "easy": 0,
        "medium": 0,
        "hard": 0,
        "expert": 0,
    }

    problem_dir = {}
    for mode in ["easy", "medium", "hard", "expert"]:
        problem_dir[mode] = {}
        for d in ["map", "pddl", "solution_sat"]:
            path = f"pddl_files/problems/sokomindplus_problems/{d}_{problem_size}x{problem_size}_{mode}"
            problem_dir[mode][d] = path
            os.makedirs(path, exist_ok=True)

    # Create planner wrapper (using your fd-lama-first helper)
    pddl_planner = _create_planner("fd-lama-first")

    while True:
        try:
            grid, robot_pos, box_positions, goal_box_indices, goal_positions = \
                generate_random_sokomindplus_map(
                    problem_size,
                    wall_prob=0.2,
                    min_total_boxes=int(problem_size*problem_size*0.06),
                    max_total_boxes=int(problem_size*problem_size*0.20),
                    min_goal_boxes=1,
                    max_goal_boxes=2,
                )
        except ValueError as e:
            # Map too crowded or otherwise unsatisfied constraints,
            # just try again.
            print(f"Failed to generate a valid map: {e}")
            continue

        # Save grid for later visualization / analysis
        np.save("sokomindplus_grid.npy", grid)

        # Build PDDL problem
        pddl_str = grid_to_pddl_sokomindplus(
            problem_size,
            grid,
            robot_pos,
            box_positions,
            goal_box_indices,
            goal_positions,
            problem_name="sokomindplus_problem",
            domain_name="sokomindplus",
            tmp_pddl_path=tmp_pddl_problem_path,
        )

        # Call Fast Downward (via your helper)
        cmd_str = pddl_planner._get_cmd_str(
            pddl_domain_file_path,
            tmp_pddl_problem_path,
            timeout=timeout["expert"],
        )
        start_time = time.time()
        output = subprocess.getoutput(cmd_str)
        pddl_planner._cleanup()

        # Clean up temporary files
        if os.path.exists(tmp_pddl_problem_path):
            os.remove(tmp_pddl_problem_path)
        if os.path.exists("sokomindplus_grid.npy"):
            os.remove("sokomindplus_grid.npy")

        time_cost = time.time() - start_time

        if "Solution found!" not in output:
            print(f"Plan not found with FD! Spent {time_cost:.2f}s.")
            continue

        # Classify difficulty based on solving time
        mode = None
        if timeout["min"] <= time_cost < timeout["easy"]:
            mode = "easy"
        elif timeout["easy"] <= time_cost < timeout["medium"]:
            mode = "medium"
        elif timeout["medium"] <= time_cost < timeout["hard"]:
            mode = "hard"
        elif timeout["hard"] <= time_cost < timeout["expert"]:
            mode = "expert"

        # Extract plan (same regex style as your original script)
        fd_plan = re.findall(r"(.+) \(\d+?\)", output.lower())

        if mode is None or not fd_plan or len(fd_plan) < min_plan_length:
            print(
                f"Problem too easy or too fast! "
                f"Time {time_cost:.2f}s, plan length {len(fd_plan)}."
            )
            continue

        if problem_idx[mode] >= MAX_PROBLEM_NUM:
            print(f"Too many {mode} problems, skipping more of this mode.")
            continue

        # Save map metadata
        idx = problem_idx[mode]
        problem_dict = {
            "grid": grid,
            "robot_pos": robot_pos,
            "box_positions": box_positions,
            "goal_box_indices": goal_box_indices,
            "goal_positions": goal_positions,
        }

        with open(
            f"{problem_dir[mode]['map']}/sokomindplus_map_{idx}.pkl", "wb"
        ) as f:
            pkl.dump(problem_dict, f)

        with open(
            f"{problem_dir[mode]['pddl']}/sokomindplus_problem_{idx}.pddl", "w"
        ) as f:
            f.write(pddl_str)

        with open(
            f"{problem_dir[mode]['solution_sat']}/sokomindplus_solution_{idx}.txt",
            "w",
        ) as f:
            for move in fd_plan:
                f.write(str(move) + "\n")

        print(
            f"Found an {mode} problem! "
            f"Solved in {time_cost:.2f}s, plan length {len(fd_plan)}."
        )
        problem_idx[mode] += 1
