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
    validate_strips_plan, IncrementalPlanner, ComplementaryPlanner, PureRelaxationPlanner, MixComplementaryPlanner


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

def visualize_one_problem(problem_map_dir, problem_idx, args):
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
    imageio.imwrite(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}"
                    f"_{args.problem_mode}_{problem_idx}_original_problem.jpg", namo_env.get_frame(highlight=False))

    assert args.planner_type in ["pure", "ploi", "cmpl", "relx", "flax"], "Unknown planner type!"

    planner = create_planner(args.test_planner_name)
    pddlgym_env_names = {"MazeNamo": "Mazenamo"}
    assert args.domain_name in pddlgym_env_names
    domain_name = pddlgym_env_names[args.domain_name]
    is_strips_domain = True

    print(f"Solving problem namo_{args.problem_size}x{args.problem_size}"
          f"_{args.problem_mode}_{problem_idx} with {args.planner_type} planner...", flush=True)
    seed = args.seed
    print("Starting seed {}".format(seed), flush=True)

    guider = create_guider(args.guider_name, args.train_planner_name,
                            1, is_strips_domain, 1, seed)
    guider.seed(seed)
    guider.train(domain_name)

    if args.planner_type == "pure":
        planner_to_test = planner
    elif args.planner_type == "ploi":
        planner_to_test = IncrementalPlanner(
            is_strips_domain=is_strips_domain,
            base_planner=planner, search_guider=guider, seed=seed)
    elif args.planner_type == "cmpl":
        planner_to_test = ComplementaryPlanner(
            is_strips_domain=is_strips_domain,
            base_planner=planner, search_guider=guider, seed=seed, 
            complementary_rules=args.cmpl_rules)
    elif args.planner_type == "flax":
        planner_to_test = MixComplementaryPlanner(
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
    start = time.time()
    try:
        if args.planner_type == "pure":
            plan = planner_to_test(env.domain, state, timeout=args.timeout)
            vis_info = {}
        else:
            plan, vis_info = planner_to_test(env.domain, state, timeout=args.timeout)
    except (PlanningTimeout, PlanningFailure) as e:
        print("\t\tPlanning failed with error: {}".format(e), flush=True)
    # Validate plan on the full test problem.
    if not validate_strips_plan(
            domain_file=env.domain.domain_fname,
            problem_file=env.problems[_idx].problem_fname,
            plan=plan):
        print("\t\tPlanning returned an invalid plan")

    print("Get plan of length {} in {:.5f} seconds".format(
        len(plan), time.time()-start), flush=True)

    np.save("namo_grid.npy", grid)
    namo_env.gen_grid(args.problem_size, args.problem_size)
    namo_env.reset()

    frames = [namo_env.get_frame(highlight=False)]
    for move in plan:
        action_name = move.__str__().split('(')[0]
        action = PDDL_ACTIONNAME_TO_INT[action_name]
        obs, rewards, dones, _, info = namo_env.step(action)
        # namo_env.render()
        frames.append(namo_env.get_frame(highlight=False))
        
    imageio.mimsave(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                    f"_{problem_idx}_{args.planner_type}_solution_{seed}.gif", frames, fps=5)

    if "gnn_ignored_objects" in vis_info and vis_info["gnn_ignored_objects"] is not None:
        _grid = get_gnn_relaxed_grid(grid.copy(), vis_info["gnn_ignored_objects"])
        np.save("namo_grid.npy", _grid)
        _vec_env: MazeNamoEnv = gym.make(
            "MiniGrid-MazeNamo-v0",
            render_mode="rgb_array",
            width=args.problem_size,
            height=args.problem_size,
            size=None,
            agent_start_dir=DIRECTIONS.index(robot_direction),
        )
        _namo_env = _vec_env.env.env
        _namo_env.gen_grid(args.problem_size, args.problem_size)
        _namo_env.reset()
        imageio.imwrite(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                        f"_{problem_idx}_{args.planner_type}_gnn-relaxed_problem_{seed}.jpg", _namo_env.get_frame(highlight=False))
        
        if args.draw_scores:
            for threshold, ignored_objects in vis_info["gnn_ignored_objects_threshold_dict"].items():
                _grid = get_gnn_relaxed_grid(grid.copy(), ignored_objects)
                np.save("namo_grid.npy", _grid)
                _vec_env: MazeNamoEnv = gym.make(
                    "MiniGrid-MazeNamo-v0",
                    render_mode="rgb_array",
                    width=args.problem_size,
                    height=args.problem_size,
                    size=None,
                    agent_start_dir=DIRECTIONS.index(robot_direction),
                )
                _namo_env = _vec_env.env.env
                _namo_env.gen_grid(args.problem_size, args.problem_size)
                _namo_env.reset()
                imageio.imwrite(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                                f"_{problem_idx}_{args.planner_type}_gnn-relaxed_problem_{seed}_{threshold:.5f}.jpg", _namo_env.get_frame(highlight=False))

    if "cmpl_ignored_objects" in vis_info and vis_info["cmpl_ignored_objects"] is not None:
        _grid = get_gnn_relaxed_grid(grid.copy(), vis_info["cmpl_ignored_objects"])
        np.save("namo_grid.npy", _grid)
        _vec_env: MazeNamoEnv = gym.make(
            "MiniGrid-MazeNamo-v0",
            # render_mode="human",
            render_mode="rgb_array",
            width=args.problem_size,
            height=args.problem_size,
            size=None,
            agent_start_dir=DIRECTIONS.index(robot_direction),
        )
        _namo_env = _vec_env.env.env
        _namo_env.gen_grid(args.problem_size, args.problem_size)
        _namo_env.reset()
        imageio.imwrite(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                        f"_{problem_idx}_{args.planner_type}_enhanced_problem_{seed}.jpg", _namo_env.get_frame(highlight=False))

    if "relx_ignored_objects" in vis_info and vis_info["relx_ignored_objects"] is not None:
        _grid = get_rule_relaxed_grid(grid.copy(), vis_info["relx_ignored_objects"])
        np.save("namo_grid.npy", _grid)
        _vec_env: MazeNamoEnv = gym.make(
            "MiniGrid-MazeNamo-v0",
            # render_mode="human",
            render_mode="rgb_array",
            width=args.problem_size,
            height=args.problem_size,
            size=None,
            agent_start_dir=DIRECTIONS.index(robot_direction),
        )
        _namo_env = _vec_env.env.env
        _namo_env.gen_grid(args.problem_size, args.problem_size)
        _namo_env.reset()
        frames = [_namo_env.get_frame(highlight=False)]
        for move in vis_info["relaxed_plan"]:
            action_name = move.__str__().split('(')[0]
            action = PDDL_ACTIONNAME_TO_INT[action_name]
            obs, rewards, dones, _, info = _namo_env.step(action)
            # _namo_env.render()
            frames.append(_namo_env.get_frame(highlight=False))

        if seed == 0:
            imageio.imwrite(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                            f"_{problem_idx}_{args.planner_type}_rule-relaxed_problem.jpg", frames[0])
        imageio.mimsave(f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                        f"_{problem_idx}_{args.planner_type}_rule-relaxed_solution_{seed}.gif", frames, fps=5)

    if args.draw_scores and "object_to_score" in vis_info and vis_info["object_to_score"] is not None:
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
                    ax.text(col + 0.5, n - 1 - row + 0.5,
                            f"{val:.4f}",
                            ha="center", va="center", fontsize=12, color="white")
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
        box_scores = np.zeros((args.problem_size, args.problem_size))
        pos_scores = np.zeros((args.problem_size, args.problem_size))

        goal_pos_name = state.goal.literals[0].variables[1].name
        x, y = (int(goal_pos_name[1:]))%args.problem_size, (int(goal_pos_name[1:]))//args.problem_size
        pos_scores[y, x] = 1.0

        for obj, score in object_to_score.items():
            # print(f"Object {obj} has score {score}")
            if obj.var_type == "object":
                x, y = (int(obj.name[1:])-1)%args.problem_size, (int(obj.name[1:])-1)//args.problem_size
                box_scores[y, x] = score
            elif obj.var_type == "pos":
                x, y = (int(obj.name[1:]))%args.problem_size, (int(obj.name[1:]))//args.problem_size
                pos_scores[y, x] = score
        plot_scores_grid(box_scores, f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                        f"_{problem_idx}_object_scores_{seed}.png")
        plot_scores_grid(pos_scores, f"{args.vis_log_dir}/namo_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
                        f"_{problem_idx}_pos_scores_{seed}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain_name", required=True, type=str)
    parser.add_argument("--problem_size", required=True, type=int)
    parser.add_argument("--problem_mode", required=True, type=str)
    parser.add_argument("--problem_idx", required=True, type=str)
    parser.add_argument("--train_planner_name", type=str, default="")
    parser.add_argument("--test_planner_name", required=True, type=str)
    parser.add_argument("--guider_name", required=True, type=str)
    parser.add_argument("--seed", required=True, type=int, default=8)
    parser.add_argument("--planner_type", required=True, type=str)
    parser.add_argument("--timeout", required=True, type=float)
    parser.add_argument("--cmpl_rules", type=str, default="config/complementary_rules.json")
    parser.add_argument("--relx_rules", type=str, default="config/relaxation_rules.json")
    parser.add_argument("--vis_log_dir", type=str, default="vis")
    parser.add_argument("--draw_scores", default=False, action="store_true",)
    args = parser.parse_args()

    problem_map_dir = f"namo_problems/map_{args.problem_size}x{args.problem_size}_{args.problem_mode}"
    if not os.path.exists(args.vis_log_dir):
        os.mkdir(args.vis_log_dir)
    if args.problem_idx == "all":
        for file_name in os.listdir(problem_map_dir):
            problem_idx = file_name.split('.')[0].split('_')[-1]
            visualize_one_problem(problem_map_dir, problem_idx, args)
    else:
        visualize_one_problem(problem_map_dir, args.problem_idx, args)
