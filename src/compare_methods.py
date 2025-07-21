import argparse
import io
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import gymnasium as gym
from minigrid.envs import MazeNamoEnv
import pickle as pkl
import imageio
from my_utils.pddl_utils import *
import pddlgym
from pddlgym.structs import LiteralConjunction
from planning import PlanningTimeout, PlanningFailure, \
    validate_strips_plan, IncrementalPlanner, MixComplementaryPlanner


def compare_one_problem(problem_map_dir, problem_idx, args):
    problem_map_file = f"{problem_map_dir}/namo_map_{problem_idx}.pkl"
    with open(problem_map_file, "rb") as f:
        problem_dict = pkl.load(f)

    grid = problem_dict["grid"]
    robot_pos = problem_dict["robot_pos"]
    robot_direction = problem_dict["robot_direction"]

    vec_env: MazeNamoEnv = gym.make(
        "MiniGrid-MazeNamo-v0",
        # render_mode="human",
        render_mode="rgb_array",
        width=args.problem_size,
        height=args.problem_size,
        size=None,
        agent_start_dir=DIRECTIONS.index(robot_direction),
    )

    namo_env = vec_env.env.env
    np.save("namo_grid.npy", grid)
    namo_env.gen_grid(args.problem_size, args.problem_size)
    namo_env.reset()

    planner = create_planner(args.test_planner_name)
    pddlgym_env_names = {"MazeNamo": "Mazenamo"}
    assert args.domain_name in pddlgym_env_names
    domain_name = pddlgym_env_names[args.domain_name]
    is_strips_domain = True

    print(f"Solving problem namo_{args.problem_size}x{args.problem_size}"
          f"_{args.problem_mode}_{problem_idx}...", flush=True)
    seed = args.seed
    print("Starting seed {}".format(seed), flush=True)

    guider = create_guider(args.guider_name, args.train_planner_name,
                            1, is_strips_domain, 1, seed)
    guider.seed(seed)
    guider.train(domain_name)

    pure_planner = planner
    ploi_planner = IncrementalPlanner(
        is_strips_domain=is_strips_domain,
        base_planner=planner, search_guider=guider, seed=seed)
    flax_planner = MixComplementaryPlanner(
        is_strips_domain=is_strips_domain,
        base_planner=planner, search_guider=guider, seed=seed, 
        complementary_rules=args.cmpl_rules, relaxation_rules=args.relx_rules)

    print("Running testing...")
    env = pddlgym.make("PDDLEnv{}-v0".format(domain_name+"Test"))
    _idx = None
    for i, prob in enumerate(env.problems):
        if f"namo_problem_{problem_idx}.pddl" in prob.problem_fname:
            _idx = i
            env.fix_problem_index(_idx)
            break
    state, _ = env.reset()
    if type(state.goal).__name__ == "Literal":
        state = state.with_goal(LiteralConjunction([state.goal]))

    # pure
    start = time.time()
    pure_plan = []
    try:
        pure_plan = pure_planner(env.domain, state, timeout=args.timeout)
    except (PlanningTimeout, PlanningFailure) as e:
        print("\t\tPlanning failed with error: {}".format(e), flush=True)
    # Validate plan on the full test problem.
    if not validate_strips_plan(
            domain_file=env.domain.domain_fname,
            problem_file=env.problems[_idx].problem_fname,
            plan=pure_plan):
        print("\t\tPlanning returned an invalid plan")
    pure_time = time.time() - start
    print("Get plan of length {} in {:.5f} seconds".format(
        len(pure_plan), pure_time), flush=True)

    # ploi
    start = time.time()
    ploi_plan = []
    try:
        ploi_plan, vis_info = ploi_planner(env.domain, state, timeout=args.timeout)
    except (PlanningTimeout, PlanningFailure) as e:
        print("\t\tPlanning failed with error: {}".format(e), flush=True)
    # Validate plan on the full test problem.
    if not validate_strips_plan(
            domain_file=env.domain.domain_fname,
            problem_file=env.problems[_idx].problem_fname,
            plan=ploi_plan):
        print("\t\tPlanning returned an invalid plan")
    ploi_time = time.time() - start
    print("Get plan of length {} in {:.5f} seconds".format(
        len(ploi_plan), ploi_time), flush=True)

    # flax
    start = time.time()
    flax_plan = []
    try:
        flax_plan, vis_info = flax_planner(env.domain, state, timeout=args.timeout)
    except (PlanningTimeout, PlanningFailure) as e:
        print("\t\tPlanning failed with error: {}".format(e), flush=True)
    # Validate plan on the full test problem.
    if not validate_strips_plan(
            domain_file=env.domain.domain_fname,
            problem_file=env.problems[_idx].problem_fname,
            plan=flax_plan):
        print("\t\tPlanning returned an invalid plan")
    flax_time = time.time() - start
    print("Get plan of length {} in {:.5f} seconds".format(
        len(flax_plan), flax_time), flush=True)
    
    return {"pure_time": round(pure_time, 2), "ploi_time": round(ploi_time, 2), "flax_time": round(flax_time, 2),
            "pure_len": len(pure_plan), "ploi_len": len(ploi_plan), "flax_len": len(flax_plan)}



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain_name", type=str, default="MazeNamo")
    parser.add_argument("--problem_size", type=int, default=15)
    parser.add_argument("--problem_mode", type=str, default="hard")
    parser.add_argument("--problem_idx", type=str, default="all")
    parser.add_argument("--train_planner_name", type=str, default="fd-opt-lmcut")
    parser.add_argument("--test_planner_name", type=str, default="fd-lama-first")
    parser.add_argument("--guider_name", type=str, default="gnn-bce-10")
    parser.add_argument("--seed", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=40)
    parser.add_argument("--cmpl_rules", type=str, default="config/complementary_rules.json")
    parser.add_argument("--relx_rules", type=str, default="config/relaxation_rules_1.json")
    args = parser.parse_args()

    problem_map_dir = f"namo_problems/map_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
    if args.problem_idx == "all":
        compare_results = {}
        for file_name in os.listdir(problem_map_dir):
            problem_idx = file_name.split('.')[0].split('_')[-1]
            compare_result = compare_one_problem(problem_map_dir, problem_idx, args)
            print(f"Problem {problem_idx}: {compare_result}")
            compare_results[f"{args.problem_size}x{args.problem_size}_{args.problem_mode}_{problem_idx}"] = compare_result
        for k, v in compare_results.items():
            print(f"{k}: {v}")
        avg_pure_time = np.mean([v["pure_time"] for v in compare_results.values()])
        avg_ploi_time = np.mean([v["ploi_time"] for v in compare_results.values()])
        avg_flax_time = np.mean([v["flax_time"] for v in compare_results.values()])
        print(f"Avg pure time: {avg_pure_time}, Avg ploi time: {avg_ploi_time}, Avg flax time: {avg_flax_time}")
    else:
        compare_result = compare_one_problem(problem_map_dir, args.problem_idx, args)
        print(compare_result)
