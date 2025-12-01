<h1 align="center">Fast Task Planning with Neuro-Symbolic Relaxation</h1><p align="center"><strong>
    <a href = "https://sairlab.org/qiweid/">Qiwei Du</a><sup>1</sup>,
    <a href = "https://jaraxxus-me.github.io/">Bowen Li</a><sup>2</sup>,
    <a href = "https://sairlab.org/yid/">Yi Du</a><sup>1</sup>,
    <a href = "https://sairlab.org/shaoshus/">Shaoshu Su</a><sup>1</sup>,
    <a href = "https://sairlab.org/taimengf/">Taimeng Fu</a><sup>1</sup>,
    <a href = "https://sairlab.org/zitongz/">Zitong Zhan</a><sup>1</sup>,
    <a href = "https://sairlab.org/zhipengz/">Zhiepeng Zhao</a><sup>1</sup>,
    <a href = "https://sairlab.org/chenw/">Chen Wang</a><sup>1</sup>
</strong></p>

<p align="center"><strong>
    <a href = "https://sairlab.org/">1: Spatial AI & Robotics (SAIR) Lab, Computer Science and Engineering, University at Buffalo</a><br>
    <a href = "https://theairlab.org/">2: AirLab, Robotics Institute, Carnegie Mellon University</a><br>

</strong></p>

<p align="center"><strong> 
    <a href = "https://arxiv.org/abs/2507.15975">&#128196; [Arxiv]</a>
</strong></p>


<img src="figs/pipeline.png" width="100%"/>

# Abstract
Real-world task planning requires long-horizon reasoning over large sets of objects with complex relationships and attributes, leading to a combinatorial explosion for classical symbolic planners. To prune the search space, recent methods prioritize searching on a simplified task only containing a few "important" objects predicted by a neural network. However, such a simple neuro-symbolic (NeSy) integration risks omitting critical objects and wasting resources on unsolvable simplified tasks. To enable **F**ast and reliable planning, we introduce a NeSy re**lax**ation strategy (**Flax**), combining neural importance prediction with symbolic expansion. Specifically, we first learn a graph neural network to predict entity importance to create a simplified task and solve it with a symbolic planner. Then, we solve a rule-relaxed task to obtain a quick rough plan, and reintegrate all referenced objects into the simplified task to recover any overlooked but essential elements. Finally, we apply complementary rules to refine the updated task, keeping it both reliable and compact. Extensive experiments are conducted on both synthetic and real-world maze navigation benchmarks where a robot must traverse through a maze and interact with movable obstacles. The results show that Flax boosts the average success rate by 20.82% and cuts mean wall-clock planning time by 17.65% compared with the state-of-the-art NeSy baseline. We expect that Flax offers a practical path toward fast, scalable, long-horizon task planning in complex environments.

**Video:**


<p align="middle">
<a href="https://youtu.be/_4DYcqwycnQ" target="_blank"><img src="figs/video_cover.jpg" width="600" border="3"/></a>
</p>

# Experiments
We propose a task called **Maze Navigation Among Movable Obstacles (MazeNamo)**. In a simplified MiniGrid environment, the scenario consists of a grid-based layout with three types of objects: walls (grey blocks), heavy boxes (blue blocks), and light boxes (yellow blocks). The agent can execute basic navigation actions, including moving forward and turning left or right, as well as three additional manipulative actions: push, pick up, and drop down. The following constraints govern object interactions:

 - Heavy boxes can only be pushed.
 - Light boxes can be both pushed and picked up.
 - Light boxes can be dropped either on the floor or on heavy boxes but cannot be placed on other light boxes.
 - At any given time, the agent can interact with only one box, meaning it cannot push or pick up multiple boxes simultaneously.

<img src="figs/mazenamo_minigrid_example.gif" width="50%"/>

# Environment Setup

Create conda environment
```
conda create -n flax python=3.10 -y
conda activate flax
pip install -r requirements.txt
```

Add MazeNamo env into Minigrid and install Minigrid
```
bash scripts/create_mazenamo_env.sh
```

# Dataset
The dataset is in `pddl_files/problems/mazenamo_problems`.
Link the training set to `pddlgym`:
```
mkdir pddlgym/pddl
ln -s $(pwd)/pddl_files/domains/mazenamo.pddl $(pwd)/pddlgym/pddl/mazenamo.pddl
ln -s $(pwd)/pddl_files/problems/mazenamo_problems/pddl_10x10_train $(pwd)/pddlgym/pddl/mazenamo
```

## (Optional) MazeNamo Problem Generation
You can also generate new datasets using:
```
python src/generate_mazenamo_problems.py
```
where problem size and problem difficulty can be changed.

# Install Plan Validation Tool (VAL)
```
bash scripts/install_VAL.sh
```

# Train and Test
Trained models are reused in batch scripts.  
All experiments use models trained on 200 10x10 problems. 
(If training hasn't been run before, weights will appear in `model/`. If `model/` already exists, training will be skipped.)
```
# run experiments with one group of settings
bash scripts/run_mazenamo.sh

# run experiments with multiple groups of settings
bash scripts/batch_run_mazenamo.sh
```

# MiniGrid Visualization
```
# generate .gif for a specific problem or all the problems of a certain group of settings
bash scripts/batch_vis_mazenamo.sh
```

# Isaac Sim Experiments
## Install Isaac Sim
```
pip install isaacsim[all]==4.5.0 --extra-index-url https://pypi.nvidia.com
pip install usd-core  # named pxr when importing, used to handle usd files
```

## Download Assets
Download usd files here:
```
https://drive.google.com/file/d/1Jg4G-aZOua9H5BjGLgwRbY28F0TyK66f/view?usp=sharing
```

The file structure should be:
```
flax/
├── assets/
│   ├── Collected_Box_A09_40x30x23cm_PR_V_NVD_01/
│   ├── Collected_...
│   ├── 2x2_warehouse_shapes.npy
│   ├── 2x2_warehouse_base_0.usd
│   └── ...
└── ...
```

## (Optional) Visualize a .usd file
First run:
```
python src/run_isaacsim_gui.py
```
Then, choose a .usd file in the GUI.

## (Optional) Generate your customized warehouse shape in Isaac Sim
For simplicity, we only used a 2x2 square warehouse as the base scene in our experiments (`assets/2x2_warehouse_shapes.npy`).
However, you can generate unique warehouse shapes using `generate_random_warehouse()` in `src/generate_isaacsim_warehouse_shape.py`, change the path of `warehouse_shapes` and run:
```
python src/generate_isaacsim_warehouse_base_scene.py
```
if you have customized requirements. You will get a .usd file of an empty warehouse (something like `assets/2x2_warehouse_base_0.usd`).

## Generate a MazeNamo scene in Isaac Sim
Generate from a grid map in `pddl_files/problems/mazenamo_problems/`:
```
python src/generate_isaacsim_scene_from_grid_map.py
```
Generate from a handcrafted scene:
```
python src/generate_isaacsim_scene_example.py
```

## Solve the MazeNamo problem in Isaac Sim using Forklift
Remember to set the initial robot direction in `solve_isaacsim_mazenamo_from_usd_forklift.py` according to the output info of `generate_isaacsim_scene_from_grid_map.py`.
```
python src/solve_isaacsim_mazenamo_from_usd_forklift.py
```
(Note: Rendering on the RTX 4090 GPU currently supports only 10×10 and 12×12 maps. Scaling up to a 15×15 map requires a 3×3 warehouse configuration; however, rendering the full scene sometimes exceeds the available GPU memory.)

<img src="figs/mazenamo_isaacsim_example.gif" width="95%"/>


# Additional Domains
We also included two more challenging domains to demonstrate the generalizability of our Flax.

## Difficult Logistics
It builds on the classic Logistics benchmark, where trucks and airplanes transport packages across a network of cities. Unlike the original domain, our variant requires **reasoning over an explicit connectivity graph of directed road and air links** rather than relying on simplified city-level abstractions. It further increases difficulty by introducing **unit-capacity vehicles, stackable packages, and locked road hubs that can only be unlocked via key packages at specific switch panels.** These additions create tight resource constraints and long-range causal dependencies, making the planning task substantially more complex than standard Logistics.

### Run experiments with the provided datasets:
```
# run experiments with one group of settings
bash scripts/run_difficultlogistics.sh
```

### (Optional) Generate your own datasets:
```
python src/generate_difficultlogistics_problems.py
```

## Sokomind Plus 
It is a challenging variant of the classic Sokoban puzzle, where an agent pushes
boxes on a grid to designated goal cells without pulling or passing through obstacles. Unlike standard
Sokoban, where all boxes are typically interchangeable, SokoMind Plus **assigns specific boxes to individual goal locations while treating the remaining boxes purely as movable obstacles.** This introduces tighter goal constraints and additional clutter, making long-horizon planning substantially harder
than in the original Sokoban setting.

### Run experiments with the provided datasets:
```
# run experiments with one group of settings
bash scripts/run_sokomindplus.sh
```

### (Optional) Generate your own datasets:
```
python src/generate_sokomindplus_problems.py
```


# Code base
Parts of this repository are derived from https://github.com/tomsilver/ploi and https://github.com/tomsilver/pddlgym. Many thanks to the original authors for sharing their code.

## Publications

If you used our code in your research, or you find our work useful, please cite us as:
```
@article{du2025fast,
  title={Fast Task Planning with Neuro-Symbolic Relaxation},
  author={Du, Qiwei and Li, Bowen and Du, Yi and Su, Shaoshu and Fu, Taimeng and Zhan, Zitong and Zhao, Zhipeng and Wang, Chen},
  journal={arXiv preprint arXiv:2507.15975},
  year={2025}
}
```