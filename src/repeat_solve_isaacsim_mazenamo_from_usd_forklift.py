import os
os.environ["OMNI_KIT_ACCEPT_EULA"] = "YES"

import math, time
import imageio
from isaacsim import SimulationApp

# Create the SimulationApp instance
simulation_app = SimulationApp({"headless": False})

import omni.usd
from isaacsim.core.api import SimulationContext
from isaacsim.core.utils.stage import open_stage
from isaacsim.core.utils.rotations import euler_angles_to_quat
from isaacsim.core.utils.viewports import set_camera_view
from isaacsim.sensors.camera import Camera
from isaacsim.util.debug_draw import _debug_draw

from my_utils import *
from my_utils.pddl_utils import *
from my_utils.isaacsim_utils import *

if __name__ == "__main__":
    max_try = 1000
    for try_idx in range(max_try):

        draw = _debug_draw.acquire_debug_draw_interface()

        problem_size = 10
        problem_mode = "hard"
        problem_idx = 0
        open_stage(f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_namo_{problem_size}_{problem_mode}_{problem_idx}.usd")
        stage = omni.usd.get_context().get_stage()

        pos_dict, obj2pos = get_object_positions(stage)
        # print("pos_dict:", pos_dict)
        # print("obj2pos:", obj2pos)
        print("Initial number of points:", len(obj2pos))

        # Create the initial set of circles
        r = 0.5 * UNIT_SIZE
        tmp_pddl_path = f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_namo_0.pddl"
        init_pos_dict = pos_dict
        args = {
            "planner_type": "ploi",
            "test_planner_name": "fd-lama-first",
            # "test_planner_name": "fd-opt-lmcut",
            "domain_name": "Mazenamo",
            "seed": 8,
            "guider_name": "gnn-bce-10",
            "train_planner_name": "fd-opt-lmcut",
            "cmpl_rules": "config/complementary_rules.json",
            "relx_rules": "config/relaxation_rules_1.json",
            "timeout": 40,
        }

        ########################################################
        # If namo scene is generated from grid map, 
        # check and change this according to the output info
        robot_direction="dirIsRight"
        ########################################################

        while True:
            tmp_pos_dict = sample_additional_positions(init_pos_dict, r)
            print("Final number of circles:", len(tmp_pos_dict))

            # Extract PDDL from IsaacSim objects and positions
            isaacsim_to_pddl(obj2pos, tmp_pos_dict, radius=r, robot_direction=robot_direction, tmp_pddl_path=tmp_pddl_path)
            link_single_pddl_file_to_pddlgym(tmp_pddl_path)

            # Solve the PDDL problem using a planner
            plan = get_solution(**args)

            if len(plan) > 0:
                pos_dict = tmp_pos_dict
                break
            
            print("Failed to find a plan. Restarting...")

        # Draw the final set of position circles and the plan path
        # draw_positions(pos_dict, r, draw_path=False, plan=None)
        # draw_positions(pos_dict, r, draw_path=True, plan=plan)

        forklift_prim = stage.GetPrimAtPath("/World/Forklift_0")
        forklift_controller = ForkliftController(
            stage=stage,
            forklift_prim=forklift_prim,
            speed_roller=SPEED_ROLLER,
            speed_back_wheel_move=SPEED_BACK_WHEEL_MOVE,
            speed_back_wheel_turning=SPEED_BACK_WHEEL_TURNING,
            h_placeonground=H_PLACEONGROUND,
            h_placeonobject=H_PLACEONOBJECT,
            h_move=H_MOVE,
        )
        isaacsim_action_list = get_isaacsim_action_list(plan, pos_dict)

        # Set perspective camera
        camera_dis = 1.24
        set_camera_view(eye=[-7.9*camera_dis, -6.5*camera_dis, 6.3*camera_dis], target=[0, -1.8, 0], camera_prim_path="/OmniverseKit_Persp")
        
        # Set cameras for video recording
        camera_0 = Camera(
            prim_path="/World/Camera_0",
            frequency=20,
            resolution=(1920, 1080),
        )
        camera_0.initialize()
        camera_0_prim = stage.GetPrimAtPath("/World/Camera_0")
        camera_0_prim.GetAttribute("focalLength").Set(18.15)
        camera_0_prim.GetAttribute("focusDistance").Set(float(400))
        set_camera_view(eye=[-7.9*camera_dis, -6.5*camera_dis, 6.3*camera_dis], target=[0, -1.8, 0], camera_prim_path="/World/Camera_0")


        robot_3d_pos = pos_dict[obj2pos["Forklift_0"]]
        if robot_direction == "dirIsLeft":
            camera_drift = (-1.75, 0)
            orientation=euler_angles_to_quat([0, math.pi/3, 0])
        elif robot_direction == "dirIsDown":
            camera_drift = (0, 1.75)
            orientation=euler_angles_to_quat([0, math.pi/3, -math.pi/2])
        elif robot_direction == "dirIsRight":
            camera_drift = (1.75, 0)
            orientation=euler_angles_to_quat([0, math.pi/3, math.pi])
        elif robot_direction == "dirIsUp":
            camera_drift = (0, -1.75)
            orientation=euler_angles_to_quat([0, math.pi/3, math.pi/2])
        forklift_camera = Camera(
            prim_path="/World/Forklift_0/body/body/camera",
            position=(robot_3d_pos[0]+camera_drift[0], robot_3d_pos[1]+camera_drift[1], 5.6),
            orientation=orientation,
            frequency=20,
            resolution=(1920, 1080),
        )
        forklift_camera.initialize()
        forklift_camera_prim = stage.GetPrimAtPath("/World/Forklift_0/body/body/camera")
        forklift_camera_prim.GetAttribute("focalLength").Set(18.15)
        forklift_camera_prim.GetAttribute("focusDistance").Set(float(400))

        # Start the physics simulation
        sim = SimulationContext()
        sim.reset()
        sim.play()

        frame_count = 0
        video_0_path = f"{os.getcwd()}/assets/persp_camera_{problem_size}x{problem_size}_{problem_mode}_{problem_idx}_try_{try_idx}.mp4"
        writer_0 = imageio.get_writer(video_0_path, fps=120, format='ffmpeg')
        video_1_path = f"{os.getcwd()}/assets/forklift_camera_{problem_size}x{problem_size}_{problem_mode}_{problem_idx}_try_{try_idx}.mp4"
        writer_1 = imageio.get_writer(video_1_path, fps=120, format='ffmpeg')
        
        start_time = time.time()
        while True:
            print("time:", time.time() - start_time)
            if time.time() - start_time > 3600:
                print("Timeout. Restarting...")
                break
            simulation_app.update()
            # time.sleep(0.001)
            if not sim._timeline.is_playing():
                continue

            frame_rgb = camera_0.get_rgb()
            if frame_rgb.shape[0] != 0:
                writer_0.append_data(frame_rgb)
            frame_rgb = forklift_camera.get_rgb()
            if frame_rgb.shape[0] != 0:
                writer_1.append_data(frame_rgb)

            forklift_controller.step(isaacsim_action_list)
            if forklift_controller.action_idx == len(isaacsim_action_list):
                break

            # if frame_count % 10 == 0 and sim._timeline.is_playing():
            #     print("translation:", forklift_controller.translation)
            #     print("rot_angle:", forklift_controller.rot_angle)
            #     print("isaacsim_action:", isaacsim_action_list[forklift_controller.action_idx])
            #     print("distance:", forklift_controller.distance)
            #     print("tgt_rot_angle:", forklift_controller.tgt_rot_angle)
            #     print("direction_adjusted:", forklift_controller.direction_adjusted)
            #     print("pre_push_done:", forklift_controller.pre_push_done)
            #     print("driving_back_done:", forklift_controller.driving_back_done)
            #     print("start_lifting:", forklift_controller.start_lifting)
            #     print("end_lifting:", forklift_controller.end_lifting)
            #     print("start_placing:", forklift_controller.start_placing)
            #     print("end_placing:", forklift_controller.end_placing)
            #     print()

            frame_count += 1
        sim.pause()
        writer_0.close()
        # simulation_app.close()
