#!/bin/bash

DOMAIN_NAME="MazeNamo"
RELX_RULES="config/relaxation_rules_1.json"

# PLANNER_TYPE="pure"
# PLANNER_TYPE="ploi"
# PLANNER_TYPE="cmpl"
# PLANNER_TYPE="relx"
PLANNER_TYPE="flax"


# PROBLEM_SIZE=10
# TIMEOUT=5

# PROBLEM_SIZE=12
# TIMEOUT=20

PROBLEM_SIZE=15
TIMEOUT=40


# DIFFICULTY="easy"
# NUM_TEST_PROBLEMS=300

# DIFFICULTY="medium"
# NUM_TEST_PROBLEMS=200

DIFFICULTY="hard"
NUM_TEST_PROBLEMS=100

if [ -L "pddlgym/pddl/mazenamo_test" ]; then
    unlink "pddlgym/pddl/mazenamo_test"
elif [ -d "pddlgym/pddl/mazenamo_test" ]; then
    rm -rf "pddlgym/pddl/mazenamo_test"
fi

ln -s $(pwd)/namo_problems/pddl_${PROBLEM_SIZE}x${PROBLEM_SIZE}_${DIFFICULTY} $(pwd)/pddlgym/pddl/mazenamo_test


if [ "$PLANNER_TYPE" = "pure" ]
then
    cmd_str="python -u src/main.py --domain_name $DOMAIN_NAME --test_planner_name fd-lama-first --guider_name no-guidance --num_seeds 1 --num_test_problems $NUM_TEST_PROBLEMS --planner_type $PLANNER_TYPE --timeout $TIMEOUT"
else
    cmd_str="python -u src/main.py --domain_name $DOMAIN_NAME --train_planner_name fd-opt-lmcut --test_planner_name fd-lama-first --guider_name gnn-bce-10 --num_seeds 10 --num_train_problems 200 --num_test_problems $NUM_TEST_PROBLEMS --planner_type $PLANNER_TYPE --timeout $TIMEOUT --num_epochs 301 --cmpl_rules config/complementary_rules.json --relx_rules $RELX_RULES"
fi

echo "Running Python command:"
echo $cmd_str
eval $cmd_str
