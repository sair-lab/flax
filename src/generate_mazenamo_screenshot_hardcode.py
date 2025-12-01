import io
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
import imageio
from my_utils.pddl_utils import *
from planning import PlanningTimeout, PlanningFailure, \
    validate_strips_plan, IncrementalPlanner, ComplementaryPlanner, FlaxPlanner
import pddlgym
from pddlgym.structs import LiteralConjunction
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# Constants for different types of grid elements
EMPTY = 0
WALL = 1
HEAVY_OBJECT = 2
LIGHT_OBJECT = 3
ROBOT = 4
GOAL = 5

DIRECTIONS = ['dirIsRight', 'dirIsDown', 'dirIsLeft', 'dirIsUp']

def generate_hardcode_map():
    # Create a grid with walls around the edges
    grid = np.array([
        [WALL, WALL,         WALL,         WALL,         WALL,   WALL],
        [WALL, LIGHT_OBJECT, EMPTY,        WALL,         EMPTY,  WALL],
        [WALL, WALL,         HEAVY_OBJECT, ROBOT,        WALL,   WALL],
        [WALL, GOAL,         LIGHT_OBJECT, LIGHT_OBJECT, EMPTY,  WALL],
        [WALL, LIGHT_OBJECT, WALL,         LIGHT_OBJECT, EMPTY,  WALL],
        [WALL, WALL,         WALL,         WALL,         WALL,   WALL],
        ], dtype=int).T

    robot_pos = (3, 2)
    robot_direction = 'dirIsDown'

    return grid, robot_pos, robot_direction

def grid_to_pddl(w, h, grid, robot_pos, robot_direction, tmp_pddl_path = "tmp_mazenamo_problem.pddl", no_wall_in_pddl = False):
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
    """(define (problem mazenamo_problem)
    (:domain mazenamo)
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

def get_gnn_relaxed_grid(grid, ignored_objects):
    size, _ = grid.shape
    for _obj in ignored_objects:
        obj = _obj.__str__().split(":")[0]
        if obj[0] == "o":
            x, y = (int(obj[1:])-1)%size, (int(obj[1:])-1)//size
            grid[x, y] = WALL
        elif obj[0] == "p":
            x, y = (int(obj[1:]))%size, (int(obj[1:]))//size
            grid[x, y] = WALL
    return grid

def get_rule_relaxed_grid(grid, ignored_objects):
    size, _ = grid.shape
    for _obj in ignored_objects:
        obj = _obj.__str__().split(":")[0]
        if obj[0] == "o":
            x, y = (int(obj[1:])-1)%size, (int(obj[1:])-1)//size
            grid[x, y] = EMPTY
    return grid

if __name__ == "__main__":
    problem_size = 6
    problem_idx = 0

    grid, robot_pos, robot_direction = generate_hardcode_map()

    # Save the grid to a .npy file
    np.save("mazenamo_grid.npy", grid)

    # print("direction", robot_direction, DIRECTIONS.index(robot_direction))
    vec_env: MazeNamoEnv = gym.make(
        "MiniGrid-MazeNamo-v0",
        render_mode="human",
        width=problem_size,
        height=problem_size,
        size=None,
        agent_start_dir=DIRECTIONS.index(robot_direction),
    )
    mazenamo_env = vec_env.env.env
    mazenamo_env.gen_grid(problem_size, problem_size)
    mazenamo_env.reset()
    imageio.imwrite(f"vis/mazenamo_{problem_size}x{problem_size}_hardcode_original_problem.jpg", mazenamo_env.get_frame(highlight=False))

    gym_grid = mazenamo_env.grid.grid
    # Convert the grid to PDDL and save the problem file in tmp_pddl_path
    pddl_str = grid_to_pddl(problem_size, problem_size, gym_grid, robot_pos, robot_direction)

    input("Please move the tmp PDDL problem file into pddlgym/pddl/mazenamo_test first, then press ENTER.")

    train_planner_name = "fd-opt-lmcut"
    test_planner_name = "fd-lama-first"
    planner_type = "flax"
    planner = create_planner(test_planner_name)
    domain_name = "Mazenamo"
    is_strips_domain = True
    guider_name = "gnn-bce-10"
    cmpl_rules = "config/complementary_rules.json"
    relx_rules = "config/relaxation_rules_1.json"
    timeout = 1
    vis_log_dir = "vis"

    print(f"Solving problem mazenamo_{problem_size}x{problem_size} with {test_planner_name} planner...", flush=True)
    for seed in range(1):
        print("Starting seed {}".format(seed), flush=True)

        guider = create_guider(guider_name, train_planner_name,
                                1, is_strips_domain, 1, seed)
        guider.seed(seed)
        guider.train(domain_name)

        if planner_type == "flax":
            planner_to_test = FlaxPlanner(
                is_strips_domain=is_strips_domain,
                base_planner=planner, search_guider=guider, seed=seed, 
                complementary_rules=cmpl_rules, relaxation_rules=relx_rules)

        print("Running testing...")
        env = pddlgym.make("PDDLEnv{}-v0".format(domain_name+"Test"))
        _idx = None
        for i, prob in enumerate(env.problems):
            if f"mazenamo_problem_{problem_idx}.pddl" in prob.problem_fname:
                _idx = i
                env.fix_problem_index(_idx)
                break
        state, _ = env.reset()
        if type(state.goal).__name__ == "Literal":
            state = state.with_goal(LiteralConjunction([state.goal]))
        start = time.time()
        try:
            if planner_type == "pure":
                plan = planner_to_test(env.domain, state, timeout=timeout)
                vis_info = {}
            else:
                plan, vis_info = planner_to_test(env.domain, state, timeout=timeout)
        except (PlanningTimeout, PlanningFailure) as e:
            print("\t\tPlanning failed with error: {}".format(e), flush=True)
            continue
        # Validate plan on the full test problem.
        if not validate_strips_plan(
                domain_file=env.domain.domain_fname,
                problem_file=env.problems[_idx].problem_fname,
                plan=plan):
            print("\t\tPlanning returned an invalid plan")
            continue

        print("Get plan of length {} in {:.5f} seconds".format(
            len(plan), time.time()-start), flush=True)
        print(plan)
        mazenamo_env.reset()

        frames = [mazenamo_env.get_frame(highlight=False)]
        for i, move in enumerate(plan):
            action_name = move.__str__().split('(')[0]
            action = PDDL_ACTIONNAME_TO_INT[action_name]
            obs, rewards, dones, _, info = _mazenamo_env.step(action)
            # _mazenamo_env.render()
            frames.append(_mazenamo_env.get_frame(highlight=False))
            print(f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_hardcode_original_problem_seed_{seed}_step_{i+1}.jpg")
            imageio.imwrite(f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_hardcode_original_problem_seed_{seed}_step_{i+1}.jpg", mazenamo_env.get_frame(highlight=False))

        if "gnn_ignored_objects" in vis_info and vis_info["gnn_ignored_objects"] is not None:
            _grid = get_gnn_relaxed_grid(grid.copy(), vis_info["gnn_ignored_objects"])
            np.save("mazenamo_grid.npy", _grid)
            _vec_env: MazeNamoEnv = gym.make(
                "MiniGrid-MazeNamo-v0",
                render_mode="rgb_array",
                width=problem_size,
                height=problem_size,
                size=None,
                agent_start_dir=DIRECTIONS.index(robot_direction),
            )
            _mazenamo_env = _vec_env.env.env
            _mazenamo_env.gen_grid(problem_size, problem_size)
            _mazenamo_env.reset()
            imageio.imwrite(f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_{problem_idx}_{planner_type}_gnn-relaxed_problem_{seed}.jpg", _mazenamo_env.get_frame(highlight=False))

            for threshold, ignored_objects in vis_info["gnn_ignored_objects_threshold_dict"].items():
                _grid = get_gnn_relaxed_grid(grid.copy(), ignored_objects)
                np.save("mazenamo_grid.npy", _grid)
                _vec_env: MazeNamoEnv = gym.make(
                    "MiniGrid-MazeNamo-v0",
                    render_mode="rgb_array",
                    width=problem_size,
                    height=problem_size,
                    size=None,
                    agent_start_dir=DIRECTIONS.index(robot_direction),
                )
                _mazenamo_env = _vec_env.env.env
                _mazenamo_env.gen_grid(problem_size, problem_size)
                _mazenamo_env.reset()
                imageio.imwrite(f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_{problem_idx}_{planner_type}_gnn-relaxed_problem_{seed}_{threshold:.5f}.jpg", _mazenamo_env.get_frame(highlight=False))

        if "cmpl_ignored_objects" in vis_info and vis_info["cmpl_ignored_objects"] is not None:
            _grid = get_gnn_relaxed_grid(grid.copy(), vis_info["cmpl_ignored_objects"])
            np.save("mazenamo_grid.npy", _grid)
            _vec_env: MazeNamoEnv = gym.make(
                "MiniGrid-MazeNamo-v0",
                # render_mode="human",
                render_mode="rgb_array",
                width=problem_size,
                height=problem_size,
                size=None,
                agent_start_dir=DIRECTIONS.index(robot_direction),
            )
            _mazenamo_env = _vec_env.env.env
            _mazenamo_env.gen_grid(problem_size, problem_size)
            _mazenamo_env.reset()
            imageio.imwrite(f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_{problem_idx}_{planner_type}_enhanced_problem_{seed}.jpg", _mazenamo_env.get_frame(highlight=False))

        if "relx_ignored_objects" in vis_info and vis_info["relx_ignored_objects"] is not None:
            _grid = get_rule_relaxed_grid(grid.copy(), vis_info["relx_ignored_objects"])
            np.save("mazenamo_grid.npy", _grid)
            _vec_env: MazeNamoEnv = gym.make(
                "MiniGrid-MazeNamo-v0",
                # render_mode="human",
                render_mode="rgb_array",
                width=problem_size,
                height=problem_size,
                size=None,
                agent_start_dir=DIRECTIONS.index(robot_direction),
            )
            _mazenamo_env = _vec_env.env.env
            _mazenamo_env.gen_grid(problem_size, problem_size)
            _mazenamo_env.reset()
            frames = [_mazenamo_env.get_frame(highlight=False)]
            for move in vis_info["relaxed_plan"]:
                action_name = move.__str__().split('(')[0]
                action = PDDL_ACTIONNAME_TO_INT[action_name]
                obs, rewards, dones, _, info = _mazenamo_env.step(action)
                # _mazenamo_env.render()
                frames.append(_mazenamo_env.get_frame(highlight=False))

            if seed == 0:
                imageio.imwrite(f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_{problem_idx}_{planner_type}_rule-relaxed_problem.jpg", frames[0])
            # imageio.mimsave(f"{args.vis_log_dir}/mazenamo_{args.problem_size}x{args.problem_size}_{problem_mode}"
            #                 f"_{problem_idx}_{args.planner_type}_rule-relaxed_solution_{seed}.gif", frames, fps=5)

        if "object_to_score" in vis_info and vis_info["object_to_score"] is not None:
            def plot_scores_grid(scores: np.ndarray, filename: str) -> None:
                n = scores.shape[0]
                cmap = mcolors.LinearSegmentedColormap.from_list(
                    "score_cmap",
                    [(0.70, 0.0, 0.0, 0.5), 
                    (0.0,  0.55, 0.0, 0.5)]
                )
                norm = mcolors.Normalize(vmin=scores.min(), vmax=scores.max())
                fig, ax = plt.subplots(figsize=(n, n), dpi=120)

                for row in range(n):
                    for col in range(n):
                        val   = scores[row, col]
                        color = cmap(norm(val))
                        ax.add_patch(
                            plt.Rectangle((col, n - 1 - row), 1, 1,
                                        facecolor=color, edgecolor="black", linewidth=0.8)
                        )
                        # ax.text(col + 0.5, n - 1 - row + 0.5,
                        #         f"{val:.4f}",
                        #         ha="center", va="center", fontsize=12, color="white")
                ax.set_xlim(0, n)
                ax.set_ylim(0, n)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_aspect("equal")
                fig.tight_layout()
                fig.canvas.draw()

                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=fig.dpi, bbox_inches="tight", pad_inches=0, transparent=True)
                buf.seek(0)
                imageio.imwrite(filename, imageio.imread(buf))
                plt.close(fig)

            object_to_score = vis_info["object_to_score"]
            box_scores = np.zeros((problem_size, problem_size))
            pos_scores = np.zeros((problem_size, problem_size))

            goal_pos_name = state.goal.literals[0].variables[1].name
            x, y = (int(goal_pos_name[1:]))%problem_size, (int(goal_pos_name[1:]))//problem_size
            pos_scores[y, x] = 1.0

            for obj, score in object_to_score.items():
                # print(f"Object {obj} has score {score}")
                if obj.var_type == "object":
                    x, y = (int(obj.name[1:])-1)%problem_size, (int(obj.name[1:])-1)//problem_size
                    box_scores[y, x] = score
                elif obj.var_type == "pos":
                    x, y = (int(obj.name[1:]))%problem_size, (int(obj.name[1:]))//problem_size
                    pos_scores[y, x] = score
            plot_scores_grid(box_scores, f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_{problem_idx}_object_scores_{seed}.png")
            plot_scores_grid(pos_scores, f"{vis_log_dir}/mazenamo_{problem_size}x{problem_size}_{problem_idx}_pos_scores_{seed}.png")




