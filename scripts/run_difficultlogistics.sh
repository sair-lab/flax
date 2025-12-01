#!/bin/bash

export PYTHONPATH=$(pwd):$PYTHONPATH
DOMAIN_NAME="DifficultLogistics"
CMPL_RULES="config/difficultlogistics_complementary_rules.json"
RELX_RULES="config/difficultlogistics_relaxation_rules_1.json"

# PLANNER_TYPE="pure"
# PLANNER_TYPE="ploi"
# PLANNER_TYPE="cmpl"
# PLANNER_TYPE="relx"
PLANNER_TYPE="flax"

TRAIN_TIMEOUT=300
NUM_TEST_PROBLEMS=300
TEST_TIMEOUT=30

if [ -L "pddlgym/pddl/difficultlogistics_test" ]; then
    unlink "pddlgym/pddl/difficultlogistics_test"
elif [ -d "pddlgym/pddl/difficultlogistics_test" ]; then
    rm -rf "pddlgym/pddl/difficultlogistics_test"
fi

ln -s $(pwd)/pddl_files/problems/difficultlogistics_problems/pddl_test $(pwd)/pddlgym/pddl/difficultlogistics_test


if [ "$PLANNER_TYPE" = "pure" ]
then
    cmd_str="python -u src/main.py --domain_name $DOMAIN_NAME --test_planner_name fd-lama-first --guider_name no-guidance --num_seeds 1 --num_test_problems $NUM_TEST_PROBLEMS --planner_type $PLANNER_TYPE --test_timeout $TEST_TIMEOUT"
else
    cmd_str="python -u src/main.py --domain_name $DOMAIN_NAME --train_planner_name fd-opt-lmcut --test_planner_name fd-lama-first --guider_name gnn-bce-10 --num_seeds 10 --num_train_problems 200 --num_test_problems $NUM_TEST_PROBLEMS --planner_type $PLANNER_TYPE --train_timeout $TRAIN_TIMEOUT --test_timeout $TEST_TIMEOUT --num_epochs 301 --cmpl_rules $CMPL_RULES --relx_rules $RELX_RULES"
fi

echo "Running Python command:"
echo $cmd_str
eval $cmd_str
