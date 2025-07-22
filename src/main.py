import os
import time
import argparse
import pddlgym
from pddlgym.structs import LiteralConjunction
from planning import PlanningTimeout, PlanningFailure, FD, \
    validate_strips_plan, verify_validate_installed, IncrementalPlanner, ComplementaryPlanner, PureRelaxationPlanner, FlaxPlanner
from guidance import NoSearchGuidance, GNNSearchGuidance
from my_utils.pddl_utils import _create_planner


def _test_planner(planner_type, planner, domain_name, num_problems, timeout):
    print("Running testing...")
    env = pddlgym.make("PDDLEnv{}-v0".format(domain_name))
    num_problems = min(num_problems, len(env.problems))

    success_num = 0
    planning_time_list = []
    plan_length_list = []
    failure_problem_list = []

    for problem_idx in range(num_problems):
        print("\tTesting problem {} of {}".format(problem_idx+1, num_problems),
              flush=True)
        env.fix_problem_index(problem_idx)
        state, _ = env.reset()
        if type(state.goal).__name__ == "Literal":
            state = state.with_goal(LiteralConjunction([state.goal]))
        start = time.time()
        try:
            if planner_type == "pure":
                plan = planner(env.domain, state, timeout=timeout)
            else:
                plan, vis_info = planner(env.domain, state, timeout=timeout)
        except (PlanningTimeout, PlanningFailure) as e:
            print("\t\tPlanning failed with error: {}".format(e), flush=True)
            failure_problem_list.append(env.problems[problem_idx].problem_fname.split("/")[-1])
            continue
        # Validate plan on the full test problem.
        if not validate_strips_plan(
                domain_file=env.domain.domain_fname,
                problem_file=env.problems[problem_idx].problem_fname,
                plan=plan):
            print("\t\tPlanning returned an invalid plan")
            continue


        planning_time = time.time()-start
        planning_time_list.append(planning_time)
        success_num += 1
        plan_length = len(plan)
        plan_length_list.append(plan_length)
        print("\t\tSuccess, got plan of length {} in {:.5f} seconds".format(
            plan_length, planning_time), flush=True)
        
        
    if success_num != 0:
        avg_planning_time = sum(planning_time_list)/success_num
        success_rate = success_num/num_problems
        avg_plan_length = sum(plan_length_list)/success_num
        print("Avg planning time: {:.5f}".format(avg_planning_time), flush=True)
        print("Success rate: {:.5f}".format(success_rate), flush=True)
        return avg_planning_time, success_rate, avg_plan_length, failure_problem_list
    else:
        return timeout, 0, 0, []


def _create_guider(guider_name, planner_name, num_train_problems,
                   is_strips_domain, num_epochs, seed):
    model_dir = os.path.join(os.path.dirname(__file__), "../model")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
    if guider_name == "no-guidance":
        return NoSearchGuidance()
    if guider_name == "gnn-bce-10":
        planner = _create_planner(planner_name)
        return GNNSearchGuidance(
            training_planner=planner,
            num_train_problems=num_train_problems,
            num_epochs=num_epochs,
            criterion_name="bce",
            bce_pos_weight=10,
            load_from_file=True,
            load_dataset_from_file=True,
            dataset_file_prefix=os.path.join(model_dir, "training_data"),
            save_model_prefix=os.path.join(
                model_dir, "bce10_model_last_seed{}".format(seed)),
            is_strips_domain=is_strips_domain,
        )
    raise Exception("Unrecognized guider name '{}'.".format(guider_name))


def _run(domain_name, train_planner_name, test_planner_name,
         guider_name, num_seeds, num_train_problems, num_test_problems,
         planner_type, timeout, num_epochs, cmpl_rules, relx_rules):
    assert verify_validate_installed(), "`validate` installation not found, please follow the README"
    print("Starting run:")
    print("\tDomain: {}".format(domain_name))
    print("\tTrain planner: {}".format(train_planner_name))
    print("\tTest planner: {}".format(test_planner_name))
    print("\tGuider: {}".format(guider_name))
    print("\tPlanner type? {}".format(planner_type))
    print("\t{} seeds, {} train problems, {} test problems".format(
        num_seeds, num_train_problems, num_test_problems), flush=True)
    print("\n\n")

    assert planner_type in ["pure", "ploi", "cmpl", "relx", "flax"], "Unknown planner type!"

    planner = _create_planner(test_planner_name)
    pddlgym_env_names = {"MazeNamo": "Mazenamo"}
    assert domain_name in pddlgym_env_names
    domain_name = pddlgym_env_names[domain_name]
    is_strips_domain = True

    planning_time_list, success_rate_list, plan_length_list = [], [], []
    total_failure_problem_set = set()
    for seed in range(num_seeds):
        print("Starting seed {}".format(seed), flush=True)

        guider = _create_guider(guider_name, train_planner_name,
                                num_train_problems, is_strips_domain,
                                num_epochs, seed)
        guider.seed(seed)
        guider.train(domain_name)

        if planner_type == "pure":
            planner_to_test = planner
        elif planner_type == "ploi":
            planner_to_test = IncrementalPlanner(
                is_strips_domain=is_strips_domain,
                base_planner=planner, search_guider=guider, seed=seed)
        elif planner_type == "cmpl":
            planner_to_test = ComplementaryPlanner(
                is_strips_domain=is_strips_domain,
                base_planner=planner, search_guider=guider, seed=seed, 
                complementary_rules=cmpl_rules)
        elif planner_type == "relx":
            planner_to_test = PureRelaxationPlanner(
                is_strips_domain=is_strips_domain,
                base_planner=planner, search_guider=guider, seed=seed, 
                relaxation_rules=relx_rules)
        elif planner_type == "flax":
            planner_to_test = FlaxPlanner(
                is_strips_domain=is_strips_domain,
                base_planner=planner, search_guider=guider, seed=seed, 
                complementary_rules=cmpl_rules, relaxation_rules=relx_rules)

        planning_time, success_rate, plan_length, failure_problem_list = _test_planner(planner_type, planner_to_test, domain_name+"Test",
                      num_problems=num_test_problems, timeout=timeout)
        planning_time_list.append(planning_time)
        success_rate_list.append(success_rate)
        plan_length_list.append(plan_length)
        total_failure_problem_set.update(failure_problem_list)
        
    print("\n\nFinished run\n\n\n\n")
    print(f"planning time list: {planning_time_list}")
    print(f"success rate list: {success_rate_list}")
    print(f"plan length list: {plan_length_list}")
    print(f"total avg planning time: {sum(planning_time_list)/num_seeds}")
    print(f"total avg success rate: {sum(success_rate_list)/num_seeds}")
    print(f"total avg plan length: {sum(plan_length_list)/num_seeds}")
    print(f"total failure problem set: {total_failure_problem_set}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain_name", required=True, type=str)
    parser.add_argument("--train_planner_name", type=str, default="")
    parser.add_argument("--test_planner_name", required=True, type=str)
    parser.add_argument("--guider_name", required=True, type=str)
    parser.add_argument("--num_seeds", required=True, type=int)
    parser.add_argument("--num_train_problems", type=int, default=0)
    parser.add_argument("--num_test_problems", required=True, type=int)
    parser.add_argument("--planner_type", required=True, type=str)
    parser.add_argument("--timeout", required=True, type=float)
    parser.add_argument("--num_epochs", type=int, default=301)
    parser.add_argument("--cmpl_rules", type=str, default="config/complementary_rules.json")
    parser.add_argument("--relx_rules", type=str, default="config/relaxation_rules.json")
    args = parser.parse_args()

    _run(args.domain_name, args.train_planner_name,
         args.test_planner_name, args.guider_name, args.num_seeds,
         args.num_train_problems, args.num_test_problems,
         args.planner_type, args.timeout, args.num_epochs,
         args.cmpl_rules, args.relx_rules)
