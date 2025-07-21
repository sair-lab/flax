import os
os.environ["OMNI_KIT_ACCEPT_EULA"] = "YES"

import math
import os
import numpy as np
from isaacsim import SimulationApp

assets_root_path = f"{os.getcwd()}/assets"

config = {
    "launch_config": {
        "renderer": "RayTracedLighting",
        "headless": True,
    },
    "warehouse_cell_center": {
        "url": f"{assets_root_path}/Collected_warehouse_h10m_center/warehouse_h10m_center.usd",
        "class": "WarehouseCellCenter",
    },
    "warehouse_cell_straight": {
        "url": f"{assets_root_path}/Collected_warehouse_h10m_straight/warehouse_h10m_straight.usd",
        "class": "WarehouseCellStraight",
    },
    "warehouse_cell_corner": {
        "url": f"{assets_root_path}/Collected_warehouse_h10m_corner_in/warehouse_h10m_corner_in.usd",
        "class": "WarehouseCellCornerIn",
    },
    "close_app_after_run": True,
}

# Create the SimulationApp instance
simulation_app = SimulationApp(launch_config=config["launch_config"])

# Late import, must be done after SimulationApp is created
from isaacsim.core.utils import prims
from isaacsim.core.utils.rotations import euler_angles_to_quat
from isaacsim.core.utils.stage import save_stage, create_new_stage
from isaacsim.core.api.objects.ground_plane import GroundPlane


WAREHOUSE_SIZE = 2
BASE_X, BASE_Y = -WAREHOUSE_SIZE * 10 / 2, -WAREHOUSE_SIZE * 10 / 2
warehouse_shapes = np.load(f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_warehouse_shapes.npy")

for i, shape in enumerate(warehouse_shapes):
    create_new_stage()
    for j in range(WAREHOUSE_SIZE):
        for k in range(WAREHOUSE_SIZE):
            print(j, k)
            print(shape[j][k])
            if shape[j][k] == 0:
                continue
            # Spawn new warehouse corner cells
            if j == 0 and k == 0 \
                or j == 0 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j][k-1] == 0 \
                or j > 0 and k == 0 and shape[j-1][k] == 0 \
                or j > 0 and k > 0 and shape[j-1][k] == 0 and shape[j][k-1] == 0:
                cell_corner_prim = prims.create_prim(
                    prim_path=f"/World/CellCorner_{j}_{k}",
                    position=(BASE_X + j * 10, BASE_Y + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, math.pi/2]),
                    usd_path=config["warehouse_cell_corner"]["url"],
                    semantic_label=config["warehouse_cell_corner"]["class"],
                )
            elif j == 0 and k == WAREHOUSE_SIZE - 1 \
                or j == 0 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j][k+1] == 0 \
                or j > 0 and k == WAREHOUSE_SIZE - 1 and shape[j-1][k] == 0 \
                or j > 0 and k < WAREHOUSE_SIZE - 1 and shape[j-1][k] == 0 and shape[j][k+1] == 0:
                cell_corner_prim = prims.create_prim(
                    prim_path=f"/World/CellCorner_{j}_{k}",
                    position=(BASE_X + j * 10, BASE_Y + 10 + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    usd_path=config["warehouse_cell_corner"]["url"],
                    semantic_label=config["warehouse_cell_corner"]["class"],
                )
            elif j == WAREHOUSE_SIZE - 1 and k == 0 \
                or j == WAREHOUSE_SIZE - 1 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j][k-1] == 0 \
                or j < WAREHOUSE_SIZE - 1 and k == 0 and shape[j+1][k] == 0 \
                or j < WAREHOUSE_SIZE - 1 and k > 0 and shape[j+1][k] == 0 and shape[j][k-1] == 0:
                cell_corner_prim = prims.create_prim(
                    prim_path=f"/World/CellCorner_{j}_{k}",
                    position=(BASE_X + 10 + j * 10, BASE_Y + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, math.pi]),
                    usd_path=config["warehouse_cell_corner"]["url"],
                    semantic_label=config["warehouse_cell_corner"]["class"],
                )
            elif j == WAREHOUSE_SIZE - 1 and k == WAREHOUSE_SIZE - 1 \
                or j == WAREHOUSE_SIZE - 1 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j][k+1] == 0 \
                or j < WAREHOUSE_SIZE - 1 and k == WAREHOUSE_SIZE - 1 and shape[j+1][k] == 0 \
                or j < WAREHOUSE_SIZE - 1 and k < WAREHOUSE_SIZE - 1 and shape[j+1][k] == 0 and shape[j][k+1] == 0:
                cell_corner_prim = prims.create_prim(
                    prim_path=f"/World/CellCorner_{j}_{k}",
                    position=(BASE_X + 10 + j * 10, BASE_Y + 10 + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, -math.pi/2]),
                    usd_path=config["warehouse_cell_corner"]["url"],
                    semantic_label=config["warehouse_cell_corner"]["class"],
                )
            # Spawn new warehouse straight cells
            elif j == 0 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j][k-1] == 1 and shape[j][k+1] == 1 \
                or j > 0 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j-1][k] == 0 and shape[j][k-1] == 1 and shape[j][k+1] == 1:
                cell_straight_prim = prims.create_prim(
                    prim_path=f"/World/CellStraight_{j}_{k}",
                    position=(BASE_X + j * 10, BASE_Y + 10 + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    usd_path=config["warehouse_cell_straight"]["url"],
                    semantic_label=config["warehouse_cell_straight"]["class"],
                )
            elif j == WAREHOUSE_SIZE - 1 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j][k-1] == 1 and shape[j][k+1] == 1 \
                or j < WAREHOUSE_SIZE - 1 and 0 < k < WAREHOUSE_SIZE - 1 and shape[j+1][k] == 0 and shape[j][k-1] == 1 and shape[j][k+1] == 1:
                cell_straight_prim = prims.create_prim(
                    prim_path=f"/World/CellStraight_{j}_{k}",
                    position=(BASE_X + 10 + j * 10, BASE_Y + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, math.pi]),
                    usd_path=config["warehouse_cell_straight"]["url"],
                    semantic_label=config["warehouse_cell_straight"]["class"],
                )
            elif k == 0 and 0 < j < WAREHOUSE_SIZE - 1 and shape[j-1][k] == 1 and shape[j+1][k] == 1 \
                or k > 0 and 0 < j < WAREHOUSE_SIZE - 1 and shape[j][k-1] == 0 and shape[j-1][k] == 1 and shape[j+1][k] == 1:
                cell_straight_prim = prims.create_prim(
                    prim_path=f"/World/CellStraight_{j}_{k}",
                    position=(BASE_X + j * 10, BASE_Y + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, math.pi/2]),
                    usd_path=config["warehouse_cell_straight"]["url"],
                    semantic_label=config["warehouse_cell_straight"]["class"],
                )
            elif k == WAREHOUSE_SIZE - 1 and 0 < j < WAREHOUSE_SIZE - 1 and shape[j-1][k] == 1 and shape[j+1][k] == 1 \
                or k < WAREHOUSE_SIZE - 1 and 0 < j < WAREHOUSE_SIZE - 1 and shape[j][k+1] == 0 and shape[j-1][k] == 1 and shape[j+1][k] == 1:
                cell_straight_prim = prims.create_prim(
                    prim_path=f"/World/CellStraight_{j}_{k}",
                    position=(BASE_X + 10 + j * 10, BASE_Y + 10 + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, -math.pi/2]),
                    usd_path=config["warehouse_cell_straight"]["url"],
                    semantic_label=config["warehouse_cell_straight"]["class"],
                )
            # Spawn new warehouse center cells
            elif 0 < j < WAREHOUSE_SIZE - 1 and 0 < k < WAREHOUSE_SIZE - 1 \
                and shape[j-1][k] == 1 and shape[j+1][k] == 1 and shape[j][k-1] == 1 and shape[j][k+1] == 1:
                cell_center_prim = prims.create_prim(
                    prim_path=f"/World/CellCenter_{j}_{k}",
                    position=(BASE_X + j * 10, BASE_Y + 10 + k * 10, 0),
                    orientation=euler_angles_to_quat([0, 0, 0]),
                    usd_path=config["warehouse_cell_center"]["url"],
                    semantic_label=config["warehouse_cell_center"]["class"],
                )

    # create a ground plane placed at 0 in the z-axis
    ground_plane = GroundPlane(prim_path="/World/GroundPlane", z_position=0, visible=False)

    print(f"Saving usd {i} into disk...")
    save_stage(f"{assets_root_path}/{WAREHOUSE_SIZE}x{WAREHOUSE_SIZE}_warehouse_base_{i}.usd")
    print(f"End Saving usd {i} into disk...")

    print(shape)
    break
