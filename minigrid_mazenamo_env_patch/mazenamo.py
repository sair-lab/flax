from __future__ import annotations

from minigrid.core.grid_3d import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import WorldObj, Goal, Wall, MoveableHeavyBox, MoveableLightBox
from minigrid.minigrid_env import MiniGridEnv
from gymnasium.core import ActType, ObsType
from typing import Any, Iterable, SupportsFloat, TypeVar
import numpy as np
from enum import IntEnum
from gymnasium import spaces

class Actions(IntEnum):
    # Turn left, turn right, move forward
    left = 0
    right = 1
    forward = 2
    # Pick up an object
    pickup = 3
    # Drop an object
    drop = 4

class MazeNamoEnv(MiniGridEnv):
    """
    ## Description

    This environment is an env for MazeNAMO, and the goal of the agent is to reach the
    green goal square, which provides a sparse reward. A small penalty is
    subtracted for the number of steps to reach the goal. This environment is
    useful, with small rooms, to validate that your RL algorithm works
    correctly, and with large rooms to experiment with sparse rewards and
    exploration. The random variants of the environment have the agent starting
    at a random position for each episode, while the regular variants have the
    agent always starting in the corner opposite to the goal.

    ## Mission Space

    "get to the green goal square"

    ## Action Space

    | Num | Name         | Action              |
    |-----|--------------|---------------------|
    | 0   | left         | Turn left           |
    | 1   | right        | Turn right          |
    | 2   | forward      | Move forward / Push |
    | 3   | pickup       | Pick up object      |
    | 4   | drop         | Place down object   |
    | 5   | toggle       | Unused              |
    | 6   | done         | Unused              |

    ## Observation Encoding

    - Each tile is encoded as a 3 dimensional tuple:
        `(OBJECT_IDX, COLOR_IDX, STATE)`
    - `OBJECT_TO_IDX` and `COLOR_TO_IDX` mapping can be found in
        [minigrid/core/constants.py](minigrid/core/constants.py)
    - `STATE` refers to the door state with 0=open, 1=closed and 2=locked

    ## Rewards

    A reward of '1 - 0.9 * (step_count / max_steps)' is given for success, and '0' for failure.

    ## Termination

    The episode ends if any one of the following conditions is met:

    1. The agent reaches the goal.
    2. Timeout (see `max_steps`).

    ## Registered Configurations

    - `MiniGrid-Namo-v0`

    """

    def __init__(
        self,
        size=10,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        agent_view_size=5,
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 1000
            # max_steps = 10 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=False,
            max_steps=max_steps,
            agent_view_size=agent_view_size,
            **kwargs,
        )

        # Action enumeration for this environment
        self.actions = Actions

        # Actions are discrete integer values
        self.action_space = spaces.Discrete(len(self.actions))

    def gen_grid(self, width, height):
        self._gen_grid(width, height)

    @staticmethod
    def _gen_mission():
        return "get to the green goal square"

    def _gen_grid(self, width, height):
        EMPTY = 0
        WALL = 1
        HEAVY_OBJECT = 2
        LIGHT_OBJECT = 3
        ROBOT = 4
        GOAL = 5

        grid_array = np.load("mazenamo_grid.npy")

        # Create an empty grid
        self.grid = Grid(width, height)

        for i in range(width):
            for j in range(height):
                if grid_array[i][j] == WALL:
                    self.put_obj(Wall(), i, j)
                elif grid_array[i][j] == HEAVY_OBJECT:
                    self.put_obj(MoveableHeavyBox("blue"), i, j)
                elif grid_array[i][j] == LIGHT_OBJECT:
                    self.put_obj(MoveableLightBox("yellow"), i, j)
                elif grid_array[i][j] == ROBOT:
                    self.agent_pos = (i, j)
                    self.agent_dir = self.agent_start_dir
                elif grid_array[i][j] == GOAL:
                    self.put_obj(Goal(), i, j)
                    self.goal_pos = (i, j)

        self.mission = "get to the green goal square"

    @property
    def front_pos_2(self):
        """
        Get the position of the cell that is 2-cell in front of the agent
        """

        return self.agent_pos + self.dir_vec * 2

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        self.step_count += 1

        reward = 0
        terminated = False
        truncated = False
        valid = True

        # Get the position in front of the agent
        fwd_pos = self.front_pos
        fwd_pos_2 = self.front_pos_2

        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)
        if 0 <= fwd_pos_2[0] < self.width and 0 <= fwd_pos_2[1] < self.height:
            fwd_cell_2 = self.grid.get(*fwd_pos_2)
        else:
            fwd_cell_2 = None
        old_pos = self.agent_pos

        # Rotate left
        if action == self.actions.left:
            self.agent_dir -= 1
            if self.agent_dir < 0:
                self.agent_dir += 4

        # Rotate right
        elif action == self.actions.right:
            self.agent_dir = (self.agent_dir + 1) % 4

        # Move forward
        elif action == self.actions.forward:
            if fwd_cell is None:
                if self.carrying is not None:
                    self.carrying.cur_pos = tuple(fwd_pos)
                    self.grid.set(self.carrying.cur_pos[0], self.carrying.cur_pos[1], self.carrying)
                    self.grid.set(self.agent_pos[0], self.agent_pos[1], None)
                self.agent_pos = tuple(fwd_pos)
            elif isinstance(fwd_cell, WorldObj):
                if self.carrying is None and "moveable" in fwd_cell.type and (fwd_cell_2 is None or fwd_cell_2.type == "goal"):
                    self.agent_pos = tuple(fwd_pos)
                    fwd_cell.cur_pos = fwd_pos_2
                    self.grid.set(fwd_pos[0], fwd_pos[1], None)
                    if fwd_cell_2 and fwd_cell_2.type == "goal":
                        self.grid.set(fwd_pos_2[0], fwd_pos_2[1], [fwd_cell_2, fwd_cell])
                    else:
                        self.grid.set(fwd_pos_2[0], fwd_pos_2[1], fwd_cell)
                elif fwd_cell is not None and fwd_cell.type == "goal":
                    if self.carrying is not None:
                        self.carrying.cur_pos = tuple(fwd_pos)
                        self.grid.set(self.carrying.cur_pos[0], self.carrying.cur_pos[1], [fwd_cell, self.carrying])
                        self.grid.set(self.agent_pos[0], self.agent_pos[1], None)
                    self.agent_pos = tuple(fwd_pos)
                    terminated = True
                    # reward = self._reward()
                    reward = 1000.0
                else:
                    valid = False
            elif isinstance(fwd_cell, list) and fwd_cell[0].type == "goal":
                if self.carrying is None and "moveable" in fwd_cell[-1].type and fwd_cell_2 is None:
                    self.agent_pos = tuple(fwd_pos)
                    fwd_cell[-1].cur_pos = fwd_pos_2
                    self.grid.set(fwd_pos[0], fwd_pos[1], fwd_cell[0])
                    self.grid.set(fwd_pos_2[0], fwd_pos_2[1], fwd_cell[-1])
                    self.agent_pos = tuple(fwd_pos)
                    terminated = True
                    # reward = self._reward()
                    reward = 1000.0
            else:
                valid = False

        # Pick up an object
        elif action == self.actions.pickup:
            if fwd_cell and self.carrying is None:
                if isinstance(fwd_cell, WorldObj):
                    if fwd_cell.can_pickup():
                        self.carrying = fwd_cell
                        # self.carrying.cur_pos = np.array([-1, -1])
                        self.carrying.cur_pos = self.agent_pos
                        self.grid.set(fwd_pos[0], fwd_pos[1], None)
                        self.grid.set(self.agent_pos[0], self.agent_pos[1], self.carrying)
                    else:
                        valid = False
                elif isinstance(fwd_cell, list):
                    if fwd_cell[-1].can_pickup():
                        self.carrying = fwd_cell[-1]
                        # self.carrying.cur_pos = np.array([-1, -1])
                        self.carrying.cur_pos = self.agent_pos
                        fwd_cell.pop()
                        if len(fwd_cell) == 1:
                            fwd_cell = fwd_cell[0]
                        self.grid.set(fwd_pos[0], fwd_pos[1], fwd_cell)
                        self.grid.set(self.agent_pos[0], self.agent_pos[1], self.carrying)
                    else:
                        valid = False
                else:
                    valid = False
            else:
                valid = False

        # Drop an object
        elif action == self.actions.drop:
            if self.carrying:
                if not fwd_cell:
                    self.grid.set(fwd_pos[0], fwd_pos[1], self.carrying)
                    self.carrying.cur_pos = fwd_pos
                    self.carrying = None
                    self.grid.set(self.agent_pos[0], self.agent_pos[1], None)
                elif isinstance(fwd_cell, WorldObj):
                    if fwd_cell.type == "moveable_heavy_box":
                        self.grid.set(fwd_pos[0], fwd_pos[1], [fwd_cell, self.carrying])
                        self.carrying.cur_pos = fwd_pos
                        self.carrying = None
                        self.grid.set(self.agent_pos[0], self.agent_pos[1], None)
                    else:
                        valid = False
                else:
                    valid = False
            else:
                valid = False

        else:
            valid = False
            raise ValueError(f"Unknown action: {action}")

        if self.step_count >= self.max_steps:
            truncated = True

        if self.render_mode == "human":
            self.render()

        obs = self.gen_obs()

        return obs, reward, terminated, truncated, {"valid": valid}

    def gen_obs(self):
        """
        Generate the agent's view (partially observable, low-resolution encoding)
        """

        grid, vis_mask = self.gen_obs_grid()

        # Encode the partially observable view into a numpy array
        image = grid.encode(vis_mask)

        # Observations are dictionaries containing:
        # - an image (partially observable view of the environment)
        # - the agent's direction/orientation (acting as a compass)
        # - a textual mission string (instructions for the agent)
        obs = {"image": image, "direction": self.agent_dir, "mission": self.mission}

        return obs