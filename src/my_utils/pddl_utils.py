import os
from guidance import NoSearchGuidance, GNNSearchGuidance
from planning import FD

DIRECTIONS = ['dirIsRight', 'dirIsDown', 'dirIsLeft', 'dirIsUp']

PDDL_ACTIONNAME_TO_INT ={
    "turnleftwhenup": 0,
    "turnleftwhendown": 0,
    "turnleftwhenleft": 0,
    "turnleftwhenright": 0,
    "turnrightwhenup": 1,
    "turnrightwhendown": 1,
    "turnrightwhenleft": 1,
    "turnrightwhenright": 1,
    "moveforwardwhenup": 2,
    "moveforwardwhendown": 2,
    "moveforwardwhenleft": 2,
    "moveforwardwhenright": 2,
    "pushobstaclewhenup": 2,
    "pushobstaclewhendown": 2,
    "pushobstaclewhenleft": 2,
    "pushobstaclewhenright": 2,
    "pickupfromgroundwhenup": 3,
    "pickupfromgroundwhendown": 3,
    "pickupfromgroundwhenleft": 3,
    "pickupfromgroundwhenright": 3,
    "pickupfromobstaclewhenup": 3,
    "pickupfromobstaclewhendown": 3,
    "pickupfromobstaclewhenleft": 3,
    "pickupfromobstaclewhenright": 3,
    "placeongroundwhenup": 4,
    "placeongroundwhendown": 4,
    "placeongroundwhenleft": 4,
    "placeongroundwhenright": 4,
    "placeonobstaclewhenup": 4,
    "placeonobstaclewhendown": 4,
    "placeonobstaclewhenleft": 4,
    "placeonobstaclewhenright": 4,
}

EMPTY = 0
WALL = 1
HEAVY_OBJECT = 2
LIGHT_OBJECT = 3
ROBOT = 4
GOAL = 5

def _create_planner(planner_name):
    if planner_name == "fd-lama-first":
        return FD(alias_flag="--alias lama-first")
    if planner_name == "fd-opt-lmcut":
        return FD(alias_flag="--alias seq-opt-lmcut")
    raise Exception("Unrecognized planner name '{}'.".format(planner_name))

def create_planner(planner_name):
    return _create_planner(planner_name)

def _create_guider(guider_name, planner_name, num_train_problems,
                   is_strips_domain, num_epochs, seed):
    if guider_name == "no-guidance":
        return NoSearchGuidance()
    if guider_name == "gnn-bce-10":
        model_dir = os.path.join(os.getcwd(), "model")
        print("model_dir: ", model_dir)
        assert os.path.exists(model_dir), "model_dir doesn't exist!"
        planner = create_planner(planner_name)
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

def create_guider(guider_name, planner_name, num_train_problems,
                    is_strips_domain, num_epochs, seed):
        return _create_guider(guider_name, planner_name, num_train_problems,
                            is_strips_domain, num_epochs, seed)