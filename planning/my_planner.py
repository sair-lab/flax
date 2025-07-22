"""An incremental planner that samples more and more objects until
it finds a plan.
"""

import time
import tempfile
import numpy as np
import json
from pddlgym.structs import State, Literal
from pddlgym.spaces import LiteralSpace
from pddlgym.parser import PDDLProblemParser
from planning import Planner, PlanningFailure, PlanningTimeout, validate_strips_plan


class IncrementalPlanner(Planner):
    """Sample objects by incrementally lowering a score threshold.
    """
    def __init__(self, is_strips_domain, base_planner, search_guider, seed,
                 gamma=0.9, # parameter for incrementing by score
                 max_iterations=1000,
                 force_include_goal_objects=True):
        super().__init__()
        assert isinstance(base_planner, Planner)
        print("Initializing {} with base planner {}, "
              "guidance {}".format(self.__class__.__name__,
                                   base_planner.__class__.__name__,
                                   search_guider.__class__.__name__))
        self._is_strips_domain = is_strips_domain
        self._gamma = gamma
        self._max_iterations = max_iterations
        self._planner = base_planner
        self._guidance = search_guider
        self._rng = np.random.RandomState(seed=seed)
        self._force_include_goal_objects = force_include_goal_objects

    def __call__(self, domain, state, timeout):
        act_preds = [domain.predicates[a] for a in list(domain.actions)]
        act_space = LiteralSpace(
            act_preds, type_to_parent_types=domain.type_to_parent_types)
        dom_file = tempfile.NamedTemporaryFile(delete=False).name
        prob_file = tempfile.NamedTemporaryFile(delete=False).name
        domain.write(dom_file)
        lits = set(state.literals)
        if not domain.operators_as_actions:
            lits |= set(act_space.all_ground_literals(
                state, valid_only=False))
        PDDLProblemParser.create_pddl_file(
            prob_file, state.objects, lits, "myproblem",
            domain.domain_name, state.goal, fast_downward_order=True)
        cur_objects = set()
        start_time = time.time()
        if self._force_include_goal_objects:
            # Always start off considering objects in the goal.
            for lit in state.goal.literals:
                cur_objects |= set(lit.variables)
        # Get scores once.
        object_to_score = {obj: self._guidance.score_object(obj, state)
                           for obj in state.objects if obj not in cur_objects}
        # Initialize threshold.
        threshold = self._gamma
        vis_info = {
            "force_include_goal_objects": cur_objects.copy(),
            "object_to_score": object_to_score,
            "gnn_ignored_objects": None,
            "gnn_ignored_objects_threshold_dict": {},
        }
        for _ in range(self._max_iterations):
            # Find new objects by incrementally lowering threshold.
            unused_objs = sorted(list(state.objects-cur_objects))
            new_objs = set()
            while unused_objs:
                # Geometrically lower threshold.
                threshold *= self._gamma
                # See if there are any new objects.
                new_objs = {o for o in unused_objs
                            if object_to_score[o] > threshold}
                # If there are, try planning with them.
                if new_objs:
                    break
            cur_objects |= new_objs
            # Keep only literals referencing currently considered objects.
            cur_lits = set()
            for lit in state.literals:
                if all(var in cur_objects for var in lit.variables):
                    cur_lits.add(lit)
            dummy_state = State(cur_lits, cur_objects, state.goal)
            # Try planning with only this object set.
            print("[Trying to plan with {} objects of {} total, "
                  "threshold is {}...]".format(len(cur_objects), len(state.objects), threshold), flush=True)
            vis_info["gnn_ignored_objects"] = state.objects - cur_objects
            vis_info["gnn_ignored_objects_threshold_dict"][threshold] = state.objects - cur_objects
            try:
                time_elapsed = time.time()-start_time
                # Get a plan from base planner & validate it.
                plan = self._planner(domain, dummy_state, timeout-time_elapsed)
                if not validate_strips_plan(domain_file=dom_file,
                                            problem_file=prob_file,
                                            plan=plan):
                    raise PlanningFailure("Invalid plan")
            except PlanningFailure:
                # Try again with more objects.
                if len(cur_objects) == len(state.objects):
                    # We already tried with all objects, give up.
                    break
                continue
            return plan, vis_info
        raise PlanningFailure("Plan not found! Reached max_iterations.")


class ComplementaryPlanner(Planner):
    """Sample objects by incrementally lowering a score threshold.
    """
    def __init__(self, is_strips_domain, base_planner, search_guider, seed,
                 gamma=0.9, # parameter for incrementing by score
                 max_iterations=1000,
                 force_include_goal_objects=True,
                 complementary_rules=None):
        super().__init__()
        assert isinstance(base_planner, Planner)
        print("Initializing {} with base planner {}, "
              "guidance {}".format(self.__class__.__name__,
                                   base_planner.__class__.__name__,
                                   search_guider.__class__.__name__))
        self._is_strips_domain = is_strips_domain
        self._gamma = gamma
        self._max_iterations = max_iterations
        self._planner = base_planner
        self._guidance = search_guider
        self._rng = np.random.RandomState(seed=seed)
        self._force_include_goal_objects = force_include_goal_objects
        with open(complementary_rules, "r") as file:
            self._complementary_rules = json.load(file)

    def __call__(self, domain, state, timeout):
        act_preds = [domain.predicates[a] for a in list(domain.actions)]
        act_space = LiteralSpace(
            act_preds, type_to_parent_types=domain.type_to_parent_types)
        dom_file = tempfile.NamedTemporaryFile(delete=False).name
        prob_file = tempfile.NamedTemporaryFile(delete=False).name
        domain.write(dom_file)
        lits = set(state.literals)
        if not domain.operators_as_actions:
            lits |= set(act_space.all_ground_literals(
                state, valid_only=False))
        PDDLProblemParser.create_pddl_file(
            prob_file, state.objects, lits, "myproblem",
            domain.domain_name, state.goal, fast_downward_order=True)
        cur_objects = set()
        start_time = time.time()
        if self._force_include_goal_objects:
            # Always start off considering objects in the goal.
            for lit in state.goal.literals:
                cur_objects |= set(lit.variables)
        # Get scores once.
        object_to_score = {obj: self._guidance.score_object(obj, state)
                           for obj in state.objects if obj not in cur_objects}
        # Initialize threshold.
        threshold = self._gamma
        vis_info = {
            "force_include_goal_objects": cur_objects.copy(),
            "object_to_score": object_to_score,
            "gnn_ignored_objects": None,
            "gnn_ignored_objects_threshold_dict": {},
            "cmpl_ignored_objects": None,
        }
        for _ in range(self._max_iterations):
            # Find new objects by incrementally lowering threshold.
            unused_objs = sorted(list(state.objects-cur_objects))
            new_objs = set()
            while unused_objs:
                # Geometrically lower threshold.
                threshold *= self._gamma
                # See if there are any new objects.
                new_objs = {o for o in unused_objs
                            if object_to_score[o] > threshold}
                # If there are, try planning with them.
                if new_objs:
                    break
            cur_objects |= new_objs
            # Keep only literals referencing currently considered objects.
            cur_lits = set()
            for lit in state.literals:
                if all(var in cur_objects for var in lit.variables):
                    cur_lits.add(lit)
            dummy_state = State(cur_lits, cur_objects, state.goal)
            # Try planning with only this object set.
            print("[Trying to plan with {} objects of {} total, "
                  "threshold is {}...]".format(len(cur_objects), len(state.objects), threshold), flush=True)
            vis_info["gnn_ignored_objects"] = state.objects - cur_objects
            vis_info["gnn_ignored_objects_threshold_dict"][threshold] = state.objects - cur_objects
            try:
                time_elapsed = time.time()-start_time
                # Get a plan from base planner & validate it.
                plan = self._planner(domain, dummy_state, timeout/2-time_elapsed)
                if not validate_strips_plan(domain_file=dom_file,
                                            problem_file=prob_file,
                                            plan=plan):
                    raise PlanningFailure("Invalid plan")
            except PlanningFailure:
                # Try again with more objects.
                # print("time spent:", time.time()-start_time)
                if len(cur_objects) == len(state.objects):
                    # We already tried with all objects, give up.
                    break
                continue
            except PlanningTimeout:
                # Try with enhanced objects.
                new_cur_objects = cur_objects.copy()
                for lit in state.literals:
                    p_name = lit.predicate.name
                    if p_name in self._complementary_rules:
                        p_cmpl_rule = self._complementary_rules[p_name]
                        for v_idx_list_cond, v_idx_list_cmpl in zip(p_cmpl_rule["cond"], p_cmpl_rule["cmpl"]):
                            if not cur_objects.isdisjoint(set([lit.variables[v_idx] for v_idx in v_idx_list_cond])):
                                new_cur_objects.update([lit.variables[v_idx] for v_idx in v_idx_list_cmpl])
                new_cur_lits = set()
                for lit in state.literals:
                    if all(var in new_cur_objects for var in lit.variables):
                        new_cur_lits.add(lit)
                dummy_state = State(new_cur_lits, new_cur_objects, state.goal)
                print("[Trying to plan with {} enhanced objects of {} total, "
                  "threshold is {}...]".format(len(new_cur_objects), len(state.objects), threshold), flush=True)
                vis_info["cmpl_ignored_objects"] = state.objects - new_cur_objects
                try:
                    time_elapsed = time.time()-start_time
                    plan = self._planner(domain, dummy_state, timeout-time_elapsed)
                except PlanningTimeout:
                    print("time spent:", time.time()-start_time)
                    raise PlanningTimeout("Planning timed out!")
         
            return plan, vis_info
        raise PlanningFailure("Plan not found! Reached max_iterations.")


class PureRelaxationPlanner(Planner):
    """Sample objects by incrementally lowering a score threshold.
    """
    def __init__(self, is_strips_domain, base_planner, search_guider, seed,
                 gamma=0.9, # parameter for incrementing by score
                 max_iterations=1000,
                 force_include_goal_objects=True,
                 relaxation_rules=None):
        super().__init__()
        assert isinstance(base_planner, Planner)
        print("Initializing {} with base planner {}, "
              "guidance {}".format(self.__class__.__name__,
                                   base_planner.__class__.__name__,
                                   search_guider.__class__.__name__))
        self._is_strips_domain = is_strips_domain
        self._gamma = gamma
        self._max_iterations = max_iterations
        self._planner = base_planner
        self._guidance = search_guider
        self._rng = np.random.RandomState(seed=seed)
        self._force_include_goal_objects = force_include_goal_objects
        with open(relaxation_rules, "r") as file:
            self._relaxation_rules = json.load(file)

    def __call__(self, domain, state, timeout):
        act_preds = [domain.predicates[a] for a in list(domain.actions)]
        act_space = LiteralSpace(
            act_preds, type_to_parent_types=domain.type_to_parent_types)
        dom_file = tempfile.NamedTemporaryFile(delete=False).name
        prob_file = tempfile.NamedTemporaryFile(delete=False).name
        domain.write(dom_file)
        lits = set(state.literals)
        if not domain.operators_as_actions:
            lits |= set(act_space.all_ground_literals(
                state, valid_only=False))
        PDDLProblemParser.create_pddl_file(
            prob_file, state.objects, lits, "myproblem",
            domain.domain_name, state.goal, fast_downward_order=True)
        cur_objects = set()
        start_time = time.time()
        if self._force_include_goal_objects:
            # Always start off considering objects in the goal.
            for lit in state.goal.literals:
                cur_objects |= set(lit.variables)
        # Get scores once.
        object_to_score = {obj: self._guidance.score_object(obj, state)
                           for obj in state.objects if obj not in cur_objects}
        # Initialize threshold.
        threshold = self._gamma
        vis_info = {
            "force_include_goal_objects": cur_objects.copy(),
            "object_to_score": object_to_score,
            "gnn_ignored_objects": None,
            "gnn_ignored_objects_threshold_dict": {},
            "relx_ignored_objects": None,
            "relaxed_plan": None,
            "cmpl_ignored_objects": None,
        }
        for _ in range(self._max_iterations):
            # Find new objects by incrementally lowering threshold.
            unused_objs = sorted(list(state.objects-cur_objects))
            new_objs = set()
            while unused_objs:
                # Geometrically lower threshold.
                threshold *= self._gamma
                # See if there are any new objects.
                new_objs = {o for o in unused_objs
                            if object_to_score[o] > threshold}
                # If there are, try planning with them.
                if new_objs:
                    break
            cur_objects |= new_objs
            # Keep only literals referencing currently considered objects.
            cur_lits = set()
            for lit in state.literals:
                if all(var in cur_objects for var in lit.variables):
                    cur_lits.add(lit)
            dummy_state = State(cur_lits, cur_objects, state.goal)
            # Try planning with only this object set.
            print("[Trying to plan with {} objects of {} total, "
                  "threshold is {}...]".format(
                      len(cur_objects), len(state.objects), threshold),
                  flush=True)
            vis_info["gnn_ignored_objects"] = state.objects - cur_objects
            vis_info["gnn_ignored_objects_threshold_dict"][threshold] = state.objects - cur_objects
            try:
                time_elapsed = time.time()-start_time
                # Get a plan from base planner & validate it.
                plan = self._planner(domain, dummy_state, timeout/6-time_elapsed)
                if not validate_strips_plan(domain_file=dom_file,
                                            problem_file=prob_file,
                                            plan=plan):
                    raise PlanningFailure("Invalid plan")
            except PlanningFailure:
                # Try again with more objects.
                # print("time spent:", time.time()-start_time)
                if len(cur_objects) == len(state.objects):
                    # We already tried with all objects, give up.
                    break
                continue
            except PlanningTimeout:
                # Try with enhanced objects.
                # Apply relaxation rules and solve the relaxed problem
                relaxed_objects = set(state.objects)
                relaxed_literals = set(state.literals)
                for rule_name in self._relaxation_rules:
                    rule = self._relaxation_rules[rule_name]
                    pre_compute_relation = {}
                    for lit in state.literals:
                        p_name = lit.predicate.name
                        if p_name in rule["pre_compute"]:
                            if p_name not in pre_compute_relation:
                                pre_compute_relation[p_name] = {}
                            v0_idx = rule["pre_compute"][p_name][0]
                            v1_idx = rule["pre_compute"][p_name][1]
                            v0, v1 = lit.variables[v0_idx], lit.variables[v1_idx]
                            pre_compute_relation[p_name][v0] = v1

                    for lit in state.literals:
                        p_name = lit.predicate.name
                        if p_name in rule["precond"]:
                            v_idx_2_obj = {}
                            for v_idx in rule["delete_objects"]:
                                v_idx_2_obj[v_idx] = lit.variables[0]
                                relaxed_objects.discard(lit.variables[0])
                            for del_p_name in rule["delete_effects"]:
                                del_p = domain.predicates[del_p_name]
                                v_idx_list = rule["delete_effects"][del_p_name]
                                if len(v_idx_list) == 1:
                                    v_idx = v_idx_list[0]
                                    relaxed_literals.discard(Literal(del_p, [v_idx_2_obj[v_idx]]))
                                elif len(v_idx_list) == 2:
                                    for v_idx in v_idx_list:
                                        if v_idx not in v_idx_2_obj:
                                            v0 = v_idx_2_obj[1-v_idx]
                                            v_idx_2_obj[v_idx] = pre_compute_relation[del_p_name][v0]
                                    relaxed_literals.discard(Literal(del_p, [v_idx_2_obj[v_idx] for v_idx in v_idx_list]))
                            for add_p_name in rule["add_effects"]:
                                add_p = domain.predicates[add_p_name]
                                v_idx_list = rule["add_effects"][add_p_name]
                                if len(v_idx_list) == 1:
                                    v_idx = v_idx_list[0]
                                    relaxed_literals.add(Literal(add_p, [v_idx_2_obj[v_idx]]))
                dummy_state = State(relaxed_literals, relaxed_objects, state.goal)
                print("[Trying to plan the rule-relaxed problem with {} objects of {} total...]".format(len(relaxed_objects), len(state.objects)), flush=True)
                vis_info["relx_ignored_objects"] = state.objects - relaxed_objects
                try:
                    time_elapsed = time.time()-start_time
                    relaxed_plan = self._planner(domain, dummy_state, timeout/2-time_elapsed)
                    vis_info["relaxed_plan"] = relaxed_plan
                except PlanningTimeout:
                    raise PlanningTimeout("Rule-relaxed problem planning timed out!")

                objects_in_relaxed_plan = {o for act in relaxed_plan for o in act.variables}
                cur_objects.update(objects_in_relaxed_plan)

                new_cur_objects = cur_objects.copy()
                # # print(f"Before applying complementary rules, cur_objects: {len(new_cur_objects)}")
                # for lit in state.literals:
                #     p_name = lit.predicate.name
                #     if p_name in self._complementary_rules:
                #         p_cmpl_rule = self._complementary_rules[p_name]
                #         for v_idx_list_cond, v_idx_list_cmpl in zip(p_cmpl_rule["cond"], p_cmpl_rule["cmpl"]):
                #             if not cur_objects.isdisjoint(set([lit.variables[v_idx] for v_idx in v_idx_list_cond])):
                #                 new_cur_objects.update([lit.variables[v_idx] for v_idx in v_idx_list_cmpl])
                new_cur_lits = set()
                for lit in state.literals:
                    if all(var in new_cur_objects for var in lit.variables):
                        new_cur_lits.add(lit)
                dummy_state = State(new_cur_lits, new_cur_objects, state.goal)
                print("[Trying to plan with {} enhanced objects of {} total, "
                  "threshold is {}...]".format(len(new_cur_objects), len(state.objects), threshold), flush=True)
                vis_info["cmpl_ignored_objects"] = state.objects - new_cur_objects
                try:
                    time_elapsed = time.time()-start_time
                    plan = self._planner(domain, dummy_state, timeout-time_elapsed)
                except PlanningTimeout:
                    print("time spent:", time.time()-start_time)
                    raise PlanningTimeout("Planning timed out!")
         
            return plan, vis_info
        raise PlanningFailure("Plan not found! Reached max_iterations.")




class FlaxPlanner(Planner):
    """Sample objects by incrementally lowering a score threshold.
    """
    def __init__(self, is_strips_domain, base_planner, search_guider, seed,
                 gamma=0.9, # parameter for incrementing by score
                 max_iterations=1000,
                 force_include_goal_objects=True,
                 complementary_rules=None,
                 relaxation_rules=None):
        super().__init__()
        assert isinstance(base_planner, Planner)
        print("Initializing {} with base planner {}, "
              "guidance {}".format(self.__class__.__name__,
                                   base_planner.__class__.__name__,
                                   search_guider.__class__.__name__))
        self._is_strips_domain = is_strips_domain
        self._gamma = gamma
        self._max_iterations = max_iterations
        self._planner = base_planner
        self._guidance = search_guider
        self._rng = np.random.RandomState(seed=seed)
        self._force_include_goal_objects = force_include_goal_objects
        with open(complementary_rules, "r") as file:
            self._complementary_rules = json.load(file)
        with open(relaxation_rules, "r") as file:
            self._relaxation_rules = json.load(file)

    def __call__(self, domain, state, timeout):
        act_preds = [domain.predicates[a] for a in list(domain.actions)]
        act_space = LiteralSpace(
            act_preds, type_to_parent_types=domain.type_to_parent_types)
        dom_file = tempfile.NamedTemporaryFile(delete=False).name
        prob_file = tempfile.NamedTemporaryFile(delete=False).name
        domain.write(dom_file)
        lits = set(state.literals)
        if not domain.operators_as_actions:
            lits |= set(act_space.all_ground_literals(
                state, valid_only=False))
        PDDLProblemParser.create_pddl_file(
            prob_file, state.objects, lits, "myproblem",
            domain.domain_name, state.goal, fast_downward_order=True)
        cur_objects = set()
        start_time = time.time()
        if self._force_include_goal_objects:
            # Always start off considering objects in the goal.
            for lit in state.goal.literals:
                cur_objects |= set(lit.variables)
        # Get scores once.
        object_to_score = {obj: self._guidance.score_object(obj, state)
                           for obj in state.objects if obj not in cur_objects}
        # Initialize threshold.
        threshold = self._gamma
        vis_info = {
            "force_include_goal_objects": cur_objects.copy(),
            "object_to_score": object_to_score,
            "gnn_ignored_objects": None,
            "gnn_ignored_objects_threshold_dict": {},
            "relx_ignored_objects": None,
            "relaxed_plan": None,
            "cmpl_ignored_objects": None,
        }
        for _ in range(self._max_iterations):
            # Find new objects by incrementally lowering threshold.
            unused_objs = sorted(list(state.objects-cur_objects))
            new_objs = set()
            while unused_objs:
                # Geometrically lower threshold.
                threshold *= self._gamma
                # See if there are any new objects.
                new_objs = {o for o in unused_objs
                            if object_to_score[o] > threshold}
                # If there are, try planning with them.
                if new_objs:
                    break
            cur_objects |= new_objs
            # Keep only literals referencing currently considered objects.
            cur_lits = set()
            for lit in state.literals:
                if all(var in cur_objects for var in lit.variables):
                    cur_lits.add(lit)
            dummy_state = State(cur_lits, cur_objects, state.goal)
            # Try planning with only this object set.
            print("[Trying to plan with {} objects of {} total, "
                  "threshold is {}...]".format(
                      len(cur_objects), len(state.objects), threshold),
                  flush=True)
            vis_info["gnn_ignored_objects"] = state.objects - cur_objects
            vis_info["gnn_ignored_objects_threshold_dict"][threshold] = state.objects - cur_objects
            try:
                time_elapsed = time.time()-start_time
                # Get a plan from base planner & validate it.
                plan = self._planner(domain, dummy_state, timeout/6-time_elapsed)
                if not validate_strips_plan(domain_file=dom_file,
                                            problem_file=prob_file,
                                            plan=plan):
                    raise PlanningFailure("Invalid plan")
            except PlanningFailure:
                # Try again with more objects.
                # print("time spent:", time.time()-start_time)
                if len(cur_objects) == len(state.objects):
                    # We already tried with all objects, give up.
                    break
                continue
            except PlanningTimeout:
                # Try with enhanced objects.
                # Apply relaxation rules and solve the relaxed problem
                relaxed_objects = set(state.objects)
                relaxed_literals = set(state.literals)
                for rule_name in self._relaxation_rules:
                    rule = self._relaxation_rules[rule_name]
                    pre_compute_relation = {}
                    for lit in state.literals:
                        p_name = lit.predicate.name
                        if p_name in rule["pre_compute"]:
                            if p_name not in pre_compute_relation:
                                pre_compute_relation[p_name] = {}
                            v0_idx = rule["pre_compute"][p_name][0]
                            v1_idx = rule["pre_compute"][p_name][1]
                            v0, v1 = lit.variables[v0_idx], lit.variables[v1_idx]
                            pre_compute_relation[p_name][v0] = v1

                    for lit in state.literals:
                        p_name = lit.predicate.name
                        if p_name in rule["precond"]:
                            v_idx_2_obj = {}
                            for v_idx in rule["delete_objects"]:
                                v_idx_2_obj[v_idx] = lit.variables[0]
                                relaxed_objects.discard(lit.variables[0])
                            for del_p_name in rule["delete_effects"]:
                                del_p = domain.predicates[del_p_name]
                                v_idx_list = rule["delete_effects"][del_p_name]
                                if len(v_idx_list) == 1:
                                    v_idx = v_idx_list[0]
                                    relaxed_literals.discard(Literal(del_p, [v_idx_2_obj[v_idx]]))
                                elif len(v_idx_list) == 2:
                                    for v_idx in v_idx_list:
                                        if v_idx not in v_idx_2_obj:
                                            v0 = v_idx_2_obj[1-v_idx]
                                            v_idx_2_obj[v_idx] = pre_compute_relation[del_p_name][v0]
                                    relaxed_literals.discard(Literal(del_p, [v_idx_2_obj[v_idx] for v_idx in v_idx_list]))
                            for add_p_name in rule["add_effects"]:
                                add_p = domain.predicates[add_p_name]
                                v_idx_list = rule["add_effects"][add_p_name]
                                if len(v_idx_list) == 1:
                                    v_idx = v_idx_list[0]
                                    relaxed_literals.add(Literal(add_p, [v_idx_2_obj[v_idx]]))
                dummy_state = State(relaxed_literals, relaxed_objects, state.goal)
                print("[Trying to plan the rule-relaxed problem with {} objects of {} total...]".format(len(relaxed_objects), len(state.objects)), flush=True)
                vis_info["relx_ignored_objects"] = state.objects - relaxed_objects
                try:
                    time_elapsed = time.time()-start_time
                    relaxed_plan = self._planner(domain, dummy_state, timeout/2-time_elapsed)
                    vis_info["relaxed_plan"] = relaxed_plan
                except PlanningTimeout:
                    raise PlanningTimeout("Rule-relaxed problem planning timed out!")

                objects_in_relaxed_plan = {o for act in relaxed_plan for o in act.variables}
                cur_objects.update(objects_in_relaxed_plan)

                # Apply complementary rules
                new_cur_objects = cur_objects.copy()
                # print(f"Before applying complementary rules, cur_objects: {len(new_cur_objects)}")
                for lit in state.literals:
                    p_name = lit.predicate.name
                    if p_name in self._complementary_rules:
                        p_cmpl_rule = self._complementary_rules[p_name]
                        for v_idx_list_cond, v_idx_list_cmpl in zip(p_cmpl_rule["cond"], p_cmpl_rule["cmpl"]):
                            if not cur_objects.isdisjoint(set([lit.variables[v_idx] for v_idx in v_idx_list_cond])):
                                new_cur_objects.update([lit.variables[v_idx] for v_idx in v_idx_list_cmpl])
                new_cur_lits = set()
                for lit in state.literals:
                    if all(var in new_cur_objects for var in lit.variables):
                        new_cur_lits.add(lit)
                dummy_state = State(new_cur_lits, new_cur_objects, state.goal)
                print("[Trying to plan with {} enhanced objects of {} total, "
                  "threshold is {}...]".format(len(new_cur_objects), len(state.objects), threshold), flush=True)
                vis_info["cmpl_ignored_objects"] = state.objects - new_cur_objects
                try:
                    time_elapsed = time.time()-start_time
                    plan = self._planner(domain, dummy_state, timeout-time_elapsed)
                except PlanningTimeout:
                    print("time spent:", time.time()-start_time)
                    raise PlanningTimeout("Planning timed out!")
         
            return plan, vis_info
        raise PlanningFailure("Plan not found! Reached max_iterations.")




