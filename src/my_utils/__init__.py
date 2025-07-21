# from .pddl_utils import *
# from .isaacsim_utils import *

import os

WAREHOUSE_SIZE = 2
assets_root_path = f"{os.getcwd()}/assets"
config = {
    "launch_config": {
        "renderer": "RayTracedLighting",
        "headless": True,
    },
    "resolution": [512, 512],
    "rt_subframes": 16,
    "num_frames": 1,
    "env_url": f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_warehouse_base_0.usd",
    "clear_previous_semantics": True,

    # walls
    "traffic_cone": {
        "url": f"{assets_root_path}/Collected_HeavyDutyTrafficCone_A05_71cm_PR_V_NVD_01/HeavyDutyTrafficCone_A05_71cm_PR_V_NVD_01.usd",
        "class": "TrafficCone",
    },
    "metal_fencing": {
        "url": f"{assets_root_path}/Collected_MetalFencing_A2/MetalFencing_A2.usd",
        "class": "MetalFencing",
    },
    "rack_long_empty": {
        "url": f"{assets_root_path}/Collected_RackLongEmpty_A2/RackLongEmpty_A2.usd",
        "class": "RackLongEmpty",
    },

    # light boxes
    "cardbox": {
        "url": f"{assets_root_path}/Collected_Cardbox_A1/Cardbox_A1.usd",
        "class": "Cardbox",
    },
    "pallet": {
        "url": f"{assets_root_path}/Collected_ExportPallet_A04_PR_NVD_01/ExportPallet_A04_PR_NVD_01.usd",
        "class": "Pallet",
    },

    # heavy boxes
    "plastic_box": {
        "url": f"{assets_root_path}/Collected_Box_A09_40x30x23cm_PR_V_NVD_01/Box_A09_40x30x23cm_PR_V_NVD_01.usd",
        "class": "PlasticBox",
    },

    # robot
    "forklift": {
        "url": f"{assets_root_path}/Collected_forklift_b/forklift_b.usd",
        "class": "Forklift",
    },

    # goal
    "goal": {
        "url": f"{assets_root_path}/Collected_GroundCloth_01/GroundCloth_01.usd",
        "class": "Goal",
    },

    "close_app_after_run": True,
}
