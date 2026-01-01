import os
import re
import shutil
os.environ["OMNI_KIT_ACCEPT_EULA"] = "YES"
# from isaacsim import SimulationApp

# # Create the SimulationApp instance
# simulation_app = SimulationApp({"headless": True})

import random, math, time
import numpy as np
import imageio

from isaacsim.core.utils.semantics import remove_all_semantics
import omni.usd
from isaacsim.util.debug_draw import _debug_draw
from pxr import Gf, Usd, UsdPhysics, UsdGeom

import pddlgym
from pddlgym.structs import LiteralConjunction
from planning import PlanningTimeout, PlanningFailure, \
    validate_strips_plan, IncrementalPlanner, ComplementaryPlanner, PureRelaxationPlanner, FlaxPlanner
from my_utils.pddl_utils import *
from my_utils import *


DIRECTIONS = ['dirIsRight', 'dirIsDown', 'dirIsLeft', 'dirIsUp']
UNIT_SIZE = 1.7
SPEED_ROLLER = 2000
SPEED_BACK_WHEEL_MOVE = 200
SPEED_BACK_WHEEL_TURNING = 10
H_PLACEONGROUND = -0.1
H_PLACEONOBJECT = 0.6
H_MOVE = 1.4


def remove_previous_semantics(stage, recursive: bool = False):
    # Clear any previous semantic data in the stage
    prims = stage.Traverse()
    for prim in prims:
        remove_all_semantics(prim, recursive)

def get_object_positions(stage):
    pos_dict = {} # mapping from position name to 2D center point
    obj2pos = {} # mapping from object name to position name
    
    bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default"])
    xform_cache = UsdGeom.XformCache(Usd.TimeCode.Default())

    for prim in stage.Traverse():
        prim_path = prim.GetPath().pathString
        prim_path_parts = prim_path.split("/")
        if len(prim_path_parts) != 3:
            continue
        prim_name = prim_path_parts[2]
        if prim.IsA(UsdGeom.Imageable) and len(prim_name.split('_')) == 2:
            # print(prim_name)
            # Compute the world-space bounding box:
            bound = bbox_cache.ComputeWorldBound(prim)
            aligned_box = bound.ComputeAlignedBox()
            min_pt = aligned_box.GetMin()
            max_pt = aligned_box.GetMax()
            # Compute center point
            center = (min_pt + max_pt) * 0.5

            if "RackLongEmpty" in prim_name:
                world_matrix = xform_cache.GetLocalToWorldTransform(prim)
                rot_angle = world_matrix.GetOrthonormalized().ExtractRotation().GetAngle()
                if abs(rot_angle) < 0.01:
                    pos_name = f"p{len(pos_dict)}"
                    pos_dict[pos_name] = (center[0], center[1]-UNIT_SIZE)
                    obj2pos[f"{prim_name}_0"] = pos_name
                    pos_name = f"p{len(pos_dict)}"
                    pos_dict[pos_name] = (center[0], center[1])
                    obj2pos[f"{prim_name}_1"] = pos_name
                    pos_name = f"p{len(pos_dict)}"
                    pos_dict[pos_name] = (center[0], center[1]+UNIT_SIZE)
                    obj2pos[f"{prim_name}_2"] = pos_name
                elif abs(rot_angle - 90) < 0.01:
                    pos_name = f"p{len(pos_dict)}"
                    pos_dict[pos_name] = (center[0]-UNIT_SIZE, center[1])
                    obj2pos[f"{prim_name}_0"] = pos_name
                    pos_name = f"p{len(pos_dict)}"
                    pos_dict[pos_name] = (center[0], center[1])
                    obj2pos[f"{prim_name}_1"] = pos_name
                    pos_name = f"p{len(pos_dict)}"
                    pos_dict[pos_name] = (center[0]+UNIT_SIZE, center[1])
                    obj2pos[f"{prim_name}_2"] = pos_name
            elif "Pallet" in prim_name:
                continue
            else:
                pos_name = f"p{len(pos_dict)}"
                pos_dict[pos_name] = (center[0], center[1])
                obj2pos[prim_name] = pos_name

    return pos_dict, obj2pos

def draw_circle(center, radius, num_segments=1024, line_width=5.0):
    # Compute points along the circle in the XY plane (z=0)
    draw = _debug_draw.acquire_debug_draw_interface()
    points = []
    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y, 0.0))

    colors = [(1, 1, 1, 1) for _ in range(num_segments)]
    sizes = [line_width for _ in range(num_segments)]
    draw.draw_points(points, colors, sizes)

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def is_valid_candidate(candidate, circles, r, tol):
    # The candidate must not overlap any circle and must be tangent to at least one.
    tangent_found = False
    for center in circles:
        d = distance(candidate, center)
        if d < 2 * r - tol:
            # Overlap detected.
            return False
        # Check for tangency (within tolerance)
        if abs(d - 2 * r) < tol:
            tangent_found = True
    return tangent_found

def sample_additional_positions(init_pos_dict, r, xmin=-10, xmax=10, ymin=-10, ymax=10):
    tmp_pos_dict = init_pos_dict.copy()
    # Randomly sample additional circles
    max_failures = 100000
    failures = 0

    while failures < max_failures:
        # Sample a random candidate within the region.
        candidate = (random.uniform(xmin, xmax), random.uniform(ymin, ymax))
        if is_valid_candidate(candidate, tmp_pos_dict.values(), r, tol=r/2):
            tmp_pos_dict[f"p{len(tmp_pos_dict)}"] = candidate
            # draw_circle(candidate, r) 
            failures = 0  # reset failure counter after a success
        else:
            failures += 1
    
    return tmp_pos_dict

def isaacsim_to_pddl(obj2pos, pos_dict, radius, robot_direction="dirIsDown", tmp_pddl_path = "assets/namo_problem.pddl"):
    objects = ["r - robot"]
    goal = [f"(rAt r {obj2pos['Goal_0']})"]
    init_state = [f"(rAt r {obj2pos['Forklift_0']})", "(handempty)", f"({robot_direction} r)"]
    pos_occupied = []
    for obj, pos in obj2pos.items():
        if obj != "Goal_0" and obj != "Forklift_0":
            objects.append(f"{obj} - object")
            init_state.append(f"(oAt {obj} {pos})")
            if "PlasticBox" in obj:
                init_state.append(f"(clear {obj})")
                init_state.append(f"(isHeavy {obj})")
                init_state.append(f"(isMoveable {obj})")
                init_state.append(f"(onGround {obj})")
            elif "Cardbox" in obj:
                init_state.append(f"(clear {obj})")
                init_state.append(f"(isLight {obj})")
                init_state.append(f"(isMoveable {obj})")
                init_state.append(f"(onGround {obj})")
            pos_occupied.append(pos)

    for pos, coord in pos_dict.items():
        objects.append(f"{pos} - pos")
        if pos not in pos_occupied:
            init_state.append(f"(posEmpty {pos})")

    for pos_1, coord_1 in pos_dict.items():
        for pos_2, coord_2 in pos_dict.items():
            if pos_1 == pos_2:
                continue
            dis = distance(coord_1, coord_2)
            x1, y1 = coord_1
            x2, y2 = coord_2
            if dis < 2.1*radius:
                if y1 > y2 and abs(x1 - x2) <= abs(y1 - y2):
                    init_state.append(f"(upTo {pos_1} {pos_2})")
                elif y1 < y2 and abs(x1 - x2) <= abs(y1 - y2):
                    init_state.append(f"(downTo {pos_1} {pos_2})")
                elif x1 < x2 and abs(y1 - y2) <= abs(x1 - x2):
                    init_state.append(f"(leftTo {pos_1} {pos_2})")
                elif x1 > x2 and abs(y1 - y2) <= abs(x1 - x2):
                    init_state.append(f"(rightTo {pos_1} {pos_2})")
            elif dis < 2.2*radius:
                if y1 > y2 and abs(x1 - x2)*2 <= abs(y1 - y2):
                    init_state.append(f"(upTo {pos_1} {pos_2})")
                elif y1 < y2 and abs(x1 - x2)*2 <= abs(y1 - y2):
                    init_state.append(f"(downTo {pos_1} {pos_2})")
                elif x1 < x2 and abs(y1 - y2)*2 <= abs(x1 - x2):
                    init_state.append(f"(leftTo {pos_1} {pos_2})")
                elif x1 > x2 and abs(y1 - y2)*2 <= abs(x1 - x2):
                    init_state.append(f"(rightTo {pos_1} {pos_2})")

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

def link_single_pddl_file_to_pddlgym(tmp_pddl_path):
    # Create a symbolic link to the PDDL file in the pddlgym pddl directory
    mazenamo_test_dir = f"{os.getcwd()}/pddlgym/pddl/mazenamo_test"
    if not os.path.exists(namo_test_dir):
        os.makedirs(namo_test_dir)
    else:
        # if this path is a symbolic link, unlink it
        if os.path.islink(namo_test_dir):
            os.unlink(namo_test_dir)
        # if this path is a dir, remove it
        elif os.path.isdir(namo_test_dir):
            shutil.rmtree(namo_test_dir)
        os.makedirs(namo_test_dir)
    # link the pddl file to the pddlgym pddl directory
    os.symlink(tmp_pddl_path, f"{namo_test_dir}/namo_problem_0.pddl")

def get_solution(planner_type, test_planner_name, domain_name, seed, guider_name, train_planner_name, cmpl_rules, relx_rules, timeout):
    assert planner_type in ["pure", "ploi", "cmpl", "relx", "flax"], "Unknown planner type!"

    planner = create_planner(test_planner_name)
    pddlgym_env_names = {"Mazenamo": "Mazenamo"}
    assert domain_name in pddlgym_env_names
    domain_name = pddlgym_env_names[domain_name]
    is_strips_domain = True

    print(f"Solving mazenamo problem from Isaac Sim with {planner_type} planner...", flush=True)

    print("Starting seed {}".format(seed), flush=True)

    guider = create_guider(guider_name, train_planner_name,
                            1, is_strips_domain, 1, seed)
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
    elif planner_type == "flax":
        planner_to_test = FlaxPlanner(
            is_strips_domain=is_strips_domain,
            base_planner=planner, search_guider=guider, seed=seed, 
            complementary_rules=cmpl_rules, relaxation_rules=relx_rules)

    print("Running testing...")
    env = pddlgym.make("PDDLEnv{}-v0".format(domain_name+"Test"))
    _idx = None
    problem_idx = 0
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
        if planner_type == "pure":
            plan = planner_to_test(env.domain, state, timeout=timeout)
            vis_info = {}
        else:
            plan, vis_info = planner_to_test(env.domain, state, timeout=timeout)
    except (PlanningTimeout, PlanningFailure) as e:
        print("\t\tPlanning failed with error: {}".format(e), flush=True)
        plan = []
    # Validate plan on the full test problem.
    if not validate_strips_plan(
            domain_file=env.domain.domain_fname,
            problem_file=env.problems[_idx].problem_fname,
            plan=plan):
        print("\t\tPlanning returned an invalid plan")

    print("Get plan of length {} in {:.5f} seconds".format(
        len(plan), time.time()-start), flush=True)

    return plan

def get_isaacsim_action_list(plan, pos_dict):
    isaacsim_action_list = []
    for action in plan:
        action_str = action.__str__()
        print(action_str)
        vars = re.findall(r'\(([^)]+)', action_str)[0].split(',')
        if "turn" in action_str:
            isaacsim_action_list.append({
                "action_name": "turn",
                "dir": re.search(r'turn(.*?)when', action_str).group(1),
            })
        elif "move" in action_str:
            x1, y1 = pos_dict[vars[1].split(':')[0]]
            x2, y2 = pos_dict[vars[2].split(':')[0]]
            isaacsim_action_list.append({
                "action_name": "move",
                "p1": Gf.Vec3d(x1, y1, 0.0),
                "p2": Gf.Vec3d(x2, y2, 0.0),
            })
        elif "push" in action_str:
            x1, y1 = pos_dict[vars[2].split(':')[0]]
            x2, y2 = pos_dict[vars[3].split(':')[0]]
            x3, y3 = pos_dict[vars[4].split(':')[0]]
            isaacsim_action_list.append({
                "action_name": "push",
                "o": vars[1].split(':')[0],
                "p1": Gf.Vec3d(x1, y1, 0.0),
                "p2": Gf.Vec3d(x2, y2, 0.0),
                "p3": Gf.Vec3d(x3, y3, 0.0),
            })
        elif "pickup" in action_str:
            x1, y1 = pos_dict[vars[2].split(':')[0]]
            x2, y2 = pos_dict[vars[3].split(':')[0]]
            isaacsim_action_list.append({
                "action_name": "pickup",
                "o": vars[1].split(':')[0],
                "p1": Gf.Vec3d(x1, y1, 0.0),
                "p2": Gf.Vec3d(x2, y2, 0.0),
            })
        elif "placeonground" in action_str:
            x1, y1 = pos_dict[vars[2].split(':')[0]]
            x2, y2 = pos_dict[vars[3].split(':')[0]]
            isaacsim_action_list.append({
                "action_name": "placeonground",
                "o": vars[1].split(':')[0],
                "p1": Gf.Vec3d(x1, y1, 0.0),
                "p2": Gf.Vec3d(x2, y2, 0.0),
            })
        elif "placeonobstacle" in action_str:
            x1, y1 = pos_dict[vars[3].split(':')[0]]
            x2, y2 = pos_dict[vars[4].split(':')[0]]
            isaacsim_action_list.append({
                "action_name": "placeonobstacle",
                "o1": vars[1].split(':')[0],
                "o2": vars[2].split(':')[0],
                "p1": Gf.Vec3d(x1, y1, 0.0),
                "p2": Gf.Vec3d(x2, y2, 0.0),
            })
    return isaacsim_action_list

def draw_positions(pos_dict, r, draw_path=False, plan=None):
    # Draw the positions as circles
    for pt in pos_dict.values():
        draw_circle(pt, r)

    # Draw the rough plan path
    if draw_path and plan is not None:
        draw = _debug_draw.acquire_debug_draw_interface()
        src_pos_list = []
        tgt_pos_list = []
        for action in plan:
            action_str = action.__str__()
            # print(action_str)
            vars = re.findall(r'\(([^)]+)', action_str)[0].split(',')
            if "move" in action_str:
                x1, y1 = pos_dict[vars[1].split(':')[0]]
                x2, y2 = pos_dict[vars[2].split(':')[0]]
                src_pos_list.append((x1, y1, 0.0))
                tgt_pos_list.append((x2, y2, 0.0))
            elif "push" in action_str:
                x1, y1 = pos_dict[vars[2].split(':')[0]]
                x2, y2 = pos_dict[vars[3].split(':')[0]]
                src_pos_list.append((x1, y1, 0.0))
                tgt_pos_list.append((x2, y2, 0.0))
        colors = [(1, 1, 1, 1) for _ in range(len(src_pos_list))]
        sizes = [5.0 for _ in range(len(src_pos_list))]
        draw.draw_lines(src_pos_list, tgt_pos_list, colors, sizes)

class ForkliftController:
    def __init__(self, stage, forklift_prim, speed_roller=2000, speed_back_wheel_move=200, 
                 speed_back_wheel_turning=10, h_placeonground=-0.1, h_placeonobject=0.6, 
                 h_move=1.0, ref_vec = Gf.Vec3d(-1, 0, 0), perp_vec = Gf.Vec3d(0, -1, 0)):
        self.forklift_prim = forklift_prim
        self.forklift_body_prim = stage.GetPrimAtPath("/World/Forklift_0/body")
        self.lift_joint_prim = forklift_prim.GetChild("lift_joint")
        self.back_wheel_drive_prim = forklift_prim.GetChild("back_wheel_joints").GetChild("back_wheel_drive")
        self.back_wheel_swivel_prim = forklift_prim.GetChild("back_wheel_joints").GetChild("back_wheel_swivel")
        self.front_right_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("front_right_roller")
        self.back_right_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("back_right_roller")
        self.front_left_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("front_left_roller")
        self.back_left_roller_prim = forklift_prim.GetChild("roller_joints").GetChild("back_left_roller")
        
        self.SPEED_ROLLER = speed_roller
        self.SPEED_BACK_WHEEL_MOVE = speed_back_wheel_move
        self.SPEED_BACK_WHEEL_TURNING = speed_back_wheel_turning
        self.H_PLACEONGROUND = h_placeonground
        self.H_PLACEONOBJECT = h_placeonobject
        self.H_MOVE = h_move
        self.REF_VEC = ref_vec
        self.PERP_VEC = perp_vec
        self.ANGLE_THRESHOLD = 0.5

        self.lift_joint_drive_api = UsdPhysics.DriveAPI.Get(self.lift_joint_prim, "linear")
        self.back_wheel_drive_drive_api = UsdPhysics.DriveAPI.Get(self.back_wheel_drive_prim, "angular")
        self.back_wheel_swivel_drive_api = UsdPhysics.DriveAPI.Get(self.back_wheel_swivel_prim, "angular")
        self.front_right_roller_drive_api = UsdPhysics.DriveAPI.Apply(self.front_right_roller_prim, "angular")
        self.back_right_roller_drive_api = UsdPhysics.DriveAPI.Apply(self.back_right_roller_prim, "angular")
        self.front_left_roller_drive_api = UsdPhysics.DriveAPI.Apply(self.front_left_roller_prim, "angular")
        self.back_left_roller_drive_api = UsdPhysics.DriveAPI.Apply(self.back_left_roller_prim, "angular")

        self.action_idx = 0
        self.direction_adjusted = False
        self.pre_push_done = False
        self.driving_back_done = False
        self.start_lifting = False
        self.end_lifting = False
        self.start_placing = False
        self.end_placing = False
        self.distance = None
        self.last_action_name = None
        self.tgt_rot_angle = None

    def step(self, isaacsim_action_list):
        forklift_world_transform_matrix = omni.usd.get_world_transform_matrix(self.forklift_body_prim)
        transform = Gf.Transform(forklift_world_transform_matrix)
        self.translation = transform.GetTranslation()
        self.rotation = transform.GetRotation()
        if self.rotation.GetAxis()[2] > 0:
            self.rot_angle = transform.GetRotation().GetAngle()
        else:
            self.rot_angle = 360 - transform.GetRotation().GetAngle()

        isaacsim_action = isaacsim_action_list[self.action_idx]
        done = False
        
        if isaacsim_action["action_name"] == "turn":
            done = True
        elif isaacsim_action["action_name"] == "move":
            done = self.move(isaacsim_action["p1"], isaacsim_action["p2"])
        elif isaacsim_action["action_name"] == "push":
            done = self.push(isaacsim_action["o"], isaacsim_action["p1"], isaacsim_action["p2"], isaacsim_action["p3"])
        elif isaacsim_action["action_name"] == "pickup":
            done = self.pickup(isaacsim_action["o"], isaacsim_action["p1"], isaacsim_action["p2"])
        elif isaacsim_action["action_name"] == "placeonground":
            done = self.place(isaacsim_action["o"], None, isaacsim_action["p1"], isaacsim_action["p2"], mode="placeonground")
        elif isaacsim_action["action_name"] == "placeonobstacle":
            done = self.place(isaacsim_action["o1"], isaacsim_action["o2"], isaacsim_action["p1"], isaacsim_action["p2"], mode="placeonobstacle")
        if done:
            self.action_idx += 1
        self.last_action_name = isaacsim_action["action_name"]

    def _turning_left(self):
        self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_BACK_WHEEL_TURNING)
        self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(90)
        self.front_right_roller_drive_api.GetTargetVelocityAttr().Set(self.SPEED_ROLLER)
        self.back_right_roller_drive_api.GetTargetVelocityAttr().Set(self.SPEED_ROLLER)
        self.front_left_roller_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_ROLLER)
        self.back_left_roller_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_ROLLER)

    def _turning_right(self):
        self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_BACK_WHEEL_TURNING)
        self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(-90)
        self.front_right_roller_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_ROLLER)
        self.back_right_roller_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_ROLLER)
        self.front_left_roller_drive_api.GetTargetVelocityAttr().Set(self.SPEED_ROLLER)
        self.back_left_roller_drive_api.GetTargetVelocityAttr().Set(self.SPEED_ROLLER)

    def _turning_end(self):
        self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
        self.front_right_roller_drive_api.GetTargetVelocityAttr().Set(0)
        self.back_right_roller_drive_api.GetTargetVelocityAttr().Set(0)
        self.front_left_roller_drive_api.GetTargetVelocityAttr().Set(0)
        self.back_left_roller_drive_api.GetTargetVelocityAttr().Set(0)

    def _get_tgt_rot_angle(self, position_diff):
        a = position_diff.GetDot(self.REF_VEC)
        b = position_diff.GetDot(self.PERP_VEC)
        tgt_rot_angle_rad = math.atan2(b, a)
        tgt_rot_angle = math.degrees(tgt_rot_angle_rad)
        if tgt_rot_angle < 0:
            tgt_rot_angle += 360
        return tgt_rot_angle

    def move(self, p1, p2):
        position_diff = p2 - self.translation
        self.distance = position_diff.GetLength()

        # Check if the forklift has reached the target position
        if self.distance < self.ANGLE_THRESHOLD:
            self.direction_adjusted = False
            return True

        # Get target rotation angle
        self.tgt_rot_angle = self._get_tgt_rot_angle(position_diff)

        # Check if the forklift has reached the target rotation angle
        if abs(self.tgt_rot_angle - self.rot_angle) < self.ANGLE_THRESHOLD:
            self.direction_adjusted = True
            self._turning_end()

        # If the forklift has not reached the target rotation angle, turn the forklift
        if not self.direction_adjusted:
            if self.rot_angle < self.tgt_rot_angle and self.tgt_rot_angle - self.rot_angle < 180 \
                or self.rot_angle > self.tgt_rot_angle and self.rot_angle - self.tgt_rot_angle > 180:
                self._turning_left()
            else:
                self._turning_right()
        # If the forklift has reached the target rotation angle, move the forklift
        else:
            self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
            self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_BACK_WHEEL_MOVE)

        return False

    def push(self, o, p1, p2, p3):
        # First, move from p1 to a position that is co-linear with 
        # the object location (p2) and the object target location (p3)
        if not self.pre_push_done:
            tgt_pre_pos = p2 - (p3 - p2)
            done = self.move(self.translation, tgt_pre_pos)
            if done:
                self.pre_push_done = True

        # Second, move from the pre-push position to the object location (p2)
        # while pushing the object
        if self.pre_push_done:
            done = self.move(self.translation, (p2 + p3) / 2)
            if done:
                self.pre_push_done = False
                return True

        return False

    def pickup(self, o, p1, p2):
        # If the forklift has ended lifting the object, 
        # move back to the original location (p1)
        if self.end_lifting:
            position_diff = self.translation - p1
        # If the forklift hasn't started lifting the object, 
        # move near the object location (p2)
        else:
            position_diff = p2 - self.translation
        self.distance = position_diff.GetLength()
        if self.distance > 10.0:
            print("Distance is too large, resetting the action")
            return True

        # Check if the forklift has reached the target position
        if self.distance < 0.1 and self.end_lifting:
            self.direction_adjusted = False
            self.driving_back_done = False
            self.start_lifting = False
            self.end_lifting = False
            return True

        # Get target rotation angle
        self.tgt_rot_angle = self._get_tgt_rot_angle(position_diff)

        # Check if the forklift has reached the target rotation angle
        if abs(self.tgt_rot_angle - self.rot_angle) < self.ANGLE_THRESHOLD:
            self.direction_adjusted = True
            self._turning_end()

        # If the forklift has not reached the target rotation angle, turn the forklift
        if not self.direction_adjusted:
            if self.rot_angle < self.tgt_rot_angle and self.tgt_rot_angle - self.rot_angle < 180 \
                or self.rot_angle > self.tgt_rot_angle and self.rot_angle - self.tgt_rot_angle > 180:
                self._turning_left()
            else:
                self._turning_right()
        # If the forklift has reached the target rotation angle, move the forklift
        else:
            # First, drive back to allow space for lowering the fork
            if not self.driving_back_done:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(self.SPEED_BACK_WHEEL_MOVE)
                if self.distance > 2.5:
                    self.driving_back_done = True
            # Second, move near the object location (p2) and lower the fork
            if self.driving_back_done and not self.start_lifting:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_BACK_WHEEL_MOVE)
                self.lift_joint_drive_api.GetTargetPositionAttr().Set(self.H_PLACEONGROUND)
                if self.distance < 0.9:
                    self.start_lifting = True
            # Third, lift the object
            if self.start_lifting and not self.end_lifting:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(0)
                self.lift_joint_drive_api.GetTargetPositionAttr().Set(self.H_MOVE)
                self.end_lifting = True
                self.direction_adjusted = False
            # Finally, move back to the original location (p1)
            if self.end_lifting:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(self.SPEED_BACK_WHEEL_MOVE)

        return False

    def place(self, o1, o2, p1, p2, mode):
        # If the forklift has ended placing the object, 
        # move back to the original location (p1)
        if self.end_placing:
            position_diff = (self.translation - p1) + (p2 - p1) * 0.6
        # If the forklift hasn't started placing the object, 
        # move near the object location (p2)
        else:
            position_diff = p2 - self.translation
        self.distance = position_diff.GetLength()

        if self.distance > 10.0:
            print("Distance is too large, resetting the action")
            return True

        # Check if the forklift has reached the target position
        if self.distance < 0.1 and self.end_placing:
        # if self.distance < 0.25 and self.end_placing:
            self.lift_joint_drive_api.GetTargetPositionAttr().Set(self.H_MOVE)
            self.direction_adjusted = False
            self.start_placing = False
            self.end_placing = False
            return True

        # Get target rotation angle
        self.tgt_rot_angle = self._get_tgt_rot_angle(position_diff)

        # Check if the forklift has reached the target rotation angle
        if abs(self.tgt_rot_angle - self.rot_angle) < self.ANGLE_THRESHOLD:
            self.direction_adjusted = True
            self._turning_end()

        # If the forklift has not reached the target rotation angle, turn the forklift
        if not self.direction_adjusted:
            if self.rot_angle < self.tgt_rot_angle and self.tgt_rot_angle - self.rot_angle < 180 \
                or self.rot_angle > self.tgt_rot_angle and self.rot_angle - self.tgt_rot_angle > 180:
                self._turning_left()
            else:
                self._turning_right()
        # If the forklift has reached the target rotation angle, move the forklift
        else:
            # First, move near the unloading location (p2) and lower the fork
            if not self.start_placing:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(-self.SPEED_BACK_WHEEL_MOVE)
                if self.distance < 1.2:
                    self.start_placing = True
            # Second, lower the fork
            if self.start_placing and not self.end_placing:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(0)
                if mode == "placeonground":
                    self.lift_joint_drive_api.GetTargetPositionAttr().Set(self.H_PLACEONGROUND)
                elif mode == "placeonobstacle":
                    self.lift_joint_drive_api.GetTargetPositionAttr().Set(self.H_PLACEONOBJECT)
                self.end_placing = True
                self.direction_adjusted = False
            # Finally, move back to the original location (p1)
            if self.end_placing:
                self.back_wheel_swivel_drive_api.GetTargetPositionAttr().Set(0)
                self.back_wheel_drive_drive_api.GetTargetVelocityAttr().Set(self.SPEED_BACK_WHEEL_MOVE)

        return False
