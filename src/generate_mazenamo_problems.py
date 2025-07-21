import re
import subprocess
import sys
import time
import numpy as np
import random
import os
import gymnasium as gym
from minigrid.envs import MazeNamoEnv
import pickle as pkl
from my_utils.pddl_utils import _create_planner

# Constants for different types of grid elements
EMPTY = 0
WALL = 1
HEAVY_OBJECT = 2
LIGHT_OBJECT = 3
ROBOT = 4
GOAL = 5

DIRECTIONS = ['dirIsRight', 'dirIsDown', 'dirIsLeft', 'dirIsUp']

def generate_random_map(size):
    # Create a grid with walls around the edges
    grid = np.zeros((size, size), dtype=int)
    grid[0, :] = WALL
    grid[-1, :] = WALL
    grid[:, 0] = WALL
    grid[:, -1] = WALL

    # Randomly place walls, heavy objects, and light objects
    for i in range(1, size-1):
        for j in range(1, size-1):
            rand_choice = random.random()
            if rand_choice < 0.2:  # 20% chance of a wall
                grid[i, j] = WALL
            elif 0.2 <= rand_choice < 0.3:  # 10% chance of a heavy object
                grid[i, j] = HEAVY_OBJECT
            elif 0.3 <= rand_choice < 0.45:  # 15% chance of a light object
                grid[i, j] = LIGHT_OBJECT

    # Place the robot in a random empty position
    robot_pos = place_randomly(grid, EMPTY)
    grid[robot_pos] = ROBOT
    robot_direction = random.choice(DIRECTIONS)

    # Place the goal in a random empty position
    goal_pos = place_randomly(grid, EMPTY)
    grid[goal_pos] = GOAL

    return grid, robot_pos, robot_direction

def place_randomly(grid, value):
    """Place an item in a random empty cell."""
    size = grid.shape[0]
    empty_positions = np.argwhere(grid == value)
    if len(empty_positions) == 0:
        raise ValueError("No empty positions left to place objects.")
    return tuple(random.choice(empty_positions))

def grid_to_pddl(w, h, grid, robot_pos, robot_direction, tmp_pddl_path = "namo_problems/namo_problem.pddl", no_wall_in_pddl = False):
    objects = ["r - robot"]
    goal = []
    init_state = ["(rAt r p{})".format(robot_pos[1] * h + robot_pos[0]), "(handempty)", "({} r)".format(robot_direction)]

    # add pos
    object_idx = 1
    for i in range(h):
        for j in range(w):
            if no_wall_in_pddl:
                if i == 0 or i == h - 1 or j == 0 or j == w - 1:
                    object_idx += 1
                    continue
            pos_idx = i * h + j
            objects.append("p{} - pos".format(pos_idx))
            o = grid[pos_idx]
            if o is not None:
                if o.type != "goal":
                    objects.append("o{} - object".format(object_idx))
                    init_state.append("(oAt o{} p{})".format(object_idx, pos_idx))
                if o.type == "moveable_heavy_box":
                    init_state.append("(isHeavy o{})".format(object_idx))
                    init_state.append("(isMoveable o{})".format(object_idx))
                    init_state.append("(onGround o{})".format(object_idx))
                    init_state.append("(clear o{})".format(object_idx))
                elif o.type == "moveable_light_box":
                    init_state.append("(isLight o{})".format(object_idx))
                    init_state.append("(isMoveable o{})".format(object_idx))
                    init_state.append("(onGround o{})".format(object_idx))
                    init_state.append("(clear o{})".format(object_idx))
                elif o.type == "goal":
                    goal.append("(rAt r p{})".format(pos_idx))
                    init_state.append("(posEmpty p{})".format(pos_idx))
            else:
                init_state.append("(posEmpty p{})".format(pos_idx))
            object_idx += 1

            if no_wall_in_pddl:
                if i < h - 2:
                    init_state.append("(upTo p{} p{})".format(pos_idx, pos_idx + w))
                if i > 1:
                    init_state.append("(downTo p{} p{})".format(pos_idx, pos_idx - w))
                if j < w - 2:
                    init_state.append("(leftTo p{} p{})".format(pos_idx, pos_idx + 1))
                if j > 1:
                    init_state.append("(rightTo p{} p{})".format(pos_idx, pos_idx - 1))
            else:
                if i < h - 1:
                    init_state.append("(upTo p{} p{})".format(pos_idx, pos_idx + w))
                if i > 0:
                    init_state.append("(downTo p{} p{})".format(pos_idx, pos_idx - w))
                if j < w - 1:
                    init_state.append("(leftTo p{} p{})".format(pos_idx, pos_idx + 1))
                if j > 0:
                    init_state.append("(rightTo p{} p{})".format(pos_idx, pos_idx - 1))

    objects = "\n\t\t".join(objects)
    goal = "\n\t\t".join(goal)
    init_state = "\n\t\t".join(init_state)

    pddl_str = \
    """(define (problem namo_problem)
    (:domain namo)
    (:objects\n\t\t{}
    )
    (:init\n\t\t{}
    )
    (:goal\n\t\t{}
    )
    )""".format(objects, init_state, goal)

    with open(tmp_pddl_path, "w") as f:
        f.write(pddl_str)
    # print("pddl_str", pddl_str)
    return pddl_str


if __name__ == "__main__":
    pddl_domain_file_path = "namo_domain.pddl"
    tmp_pddl_problem_path = "namo_problems/namo_problem.pddl"
    MAX_PROBLEM_NUM = 500

    problem_size = 15
    if problem_size == 10:
        timeout = {
            "min": 0.1,
            "easy": 2,
            "medium": 6,
            "hard": 10,
            "expert": 30,
        }
    elif problem_size == 12:
        timeout = {
            "min": 3,
            "easy": 10,
            "medium": 25,
            "hard": 40,
            "expert": 120,
        }
    elif problem_size == 15:
        timeout = {
            "min": 10,
            "easy": 30,
            "medium": 60,
            "hard": 120,
            "expert": 300,
        }
    min_plan_length = int(0.1 * problem_size**2)

    problem_idx = {
        "easy": 0,
        "medium": 0,
        "hard": 0,
        "expert": 0,
    }
    problem_dir = {}
    for mode in ["easy", "medium", "hard", "expert"]:
        problem_dir[mode] = {}
        for dir in ["map", "pddl", "solution_sat"]:
            problem_dir[mode][dir] = f"namo_problems/{dir}_{problem_size}x{problem_size}_{mode}"
            if not os.path.exists(problem_dir[mode][dir]):
                os.makedirs(problem_dir[mode][dir])
    
    pddl_planner = _create_planner("fd-lama-first")

    while True:
        grid, robot_pos, robot_direction = generate_random_map(problem_size)

        # Save the grid to a .npy file
        np.save("namo_grid.npy", grid)

        # print("direction", robot_direction, DIRECTIONS.index(robot_direction))
        vec_env: MazeNamoEnv = gym.make(
            "MiniGrid-MazeNamoEnv-v0",
            render_mode="human",
            width=problem_size,
            height=problem_size,
            size=None,
            agent_start_dir=DIRECTIONS.index(robot_direction),
        )
        namo_env = vec_env.env.env
        namo_env.gen_grid(problem_size, problem_size)

        gym_grid = namo_env.grid.grid

        # Convert the grid to PDDL and save the problem file in tmp_pddl_path
        pddl_str = grid_to_pddl(problem_size, problem_size, gym_grid, robot_pos, robot_direction)

        cmd_str = pddl_planner._get_cmd_str(pddl_domain_file_path, tmp_pddl_problem_path, timeout=timeout["expert"])
        start_time = time.time()
        output = subprocess.getoutput(cmd_str)
        pddl_planner._cleanup()
        os.remove(tmp_pddl_problem_path)
        os.remove("namo_grid.npy")

        time_cost = time.time() - start_time

        if "Solution found!" not in output:
            print(f"Plan not found with FD! Spent {time_cost}s.")
            continue

        mode = None
        if time_cost >= timeout["min"] and time_cost < timeout["easy"]:
            mode = "easy"
        elif time_cost >= timeout["easy"] and time_cost < timeout["medium"]:
            mode = "medium"
        elif time_cost >= timeout["medium"] and time_cost < timeout["hard"]:
            mode = "hard"
        elif time_cost >= timeout["hard"] and time_cost < timeout["expert"]:
            mode = "expert"

        fd_plan = re.findall(r"(.+) \(\d+?\)", output.lower())
        if mode is None or not fd_plan or len(fd_plan) < min_plan_length:
            print(f"Problem too easy! Spent {time_cost}s. Plan length {len(fd_plan)}.")
            continue

        if problem_idx[mode] >= MAX_PROBLEM_NUM:
            print(f"Too many {mode} problems!")
            continue

        problem_dict = {
            "grid": grid,
            "robot_pos": robot_pos,
            "robot_direction": robot_direction,
        }

        with open(f"{problem_dir[mode]['map']}/namo_map_{problem_idx[mode]}.pkl", "wb") as f:
            pkl.dump(problem_dict, f)

        with open(f"{problem_dir[mode]['pddl']}/namo_problem_{problem_idx[mode]}.pddl", "w") as f:
            f.write(pddl_str)
        
        with open(f"{problem_dir[mode]['solution_sat']}/namo_solution_{problem_idx[mode]}.txt", "w") as f:
            for move in fd_plan:
                f.write(str(move) + '\n')
        print(f"Find a/an {mode} problem! Solved in {time_cost}s. Plan length {len(fd_plan)}.")
        problem_idx[mode] += 1
