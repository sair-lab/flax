#!/bin/bash
DOMAIN_NAME="MazeNamo"

run_experiment() {
    local PROBLEM_SIZE="$1"         # e.g., 10, 12, 15
    local DIFFICULTY="$2"           # e.g., easy, medium, hard, expert
    local TIMEOUT="$3"              # e.g., 5, 20, 40
    local NUM_TEST_PROBLEMS="$4"    # e.g., 300, 200, 100
    local PLANNER_TYPE="$5"         # e.g., pure, ploi, cmpl, relx, flax

    local BASE_DIR
    BASE_DIR="$(pwd)"

    # Remove the old symlink (if any) and create a new one.
    if [ -L "${BASE_DIR}/pddlgym/pddl/mazenamo_test" ]; then
        unlink "${BASE_DIR}/pddlgym/pddl/mazenamo_test"
    elif [ -d "${BASE_DIR}/pddlgym/pddl/mazenamo_test" ]; then
        rm -rf "${BASE_DIR}/pddlgym/pddl/mazenamo_test"
    fi

    ln -s "${BASE_DIR}/namo_problems/pddl_${PROBLEM_SIZE}x${PROBLEM_SIZE}_${DIFFICULTY}" "${BASE_DIR}/pddlgym/pddl/mazenamo_test"

    # Build the Python command. For the "pure" planner we run a simplified command,
    # otherwise we include training options.
    local cmd_str=""
    if [ "$PLANNER_TYPE" = "pure" ]; then
        cmd_str="python -u src/main.py --domain_name ${DOMAIN_NAME} \
            --test_planner_name fd-lama-first --guider_name no-guidance --num_seeds 1 \
            --num_test_problems ${NUM_TEST_PROBLEMS} --planner_type ${PLANNER_TYPE} --timeout ${TIMEOUT}"
    else
        cmd_str="python -u src/main.py --domain_name ${DOMAIN_NAME} \
            --train_planner_name fd-opt-lmcut --test_planner_name fd-lama-first \
            --guider_name gnn-bce-10 --num_seeds 10 --num_train_problems 200 \
            --num_test_problems ${NUM_TEST_PROBLEMS} --planner_type ${PLANNER_TYPE} \
            --timeout ${TIMEOUT} --num_epochs 301 \
            --cmpl_rules config/complementary_rules.json --relx_rules config/relaxation_rules_1.json"
    fi

    echo "Running Python command:"
    echo "${cmd_str}"
    eval "${cmd_str}"
}

# Define the list of configurations.
# Each entry: "PROBLEM_SIZE DIFFICULTY TIMEOUT NUM_TEST_PROBLEMS PLANNER_TYPE"
# Note that not all combinations are needed.
experiments=(
    "10 expert 5 100 pure"
    "10 expert 5 100 ploi"
    "10 expert 5 100 cmpl"
    "10 expert 5 100 relx"
    "10 expert 5 100 flax"
    # "12 expert 20 100 pure"
    # "12 expert 20 100 ploi"
    # "12 expert 20 100 cmpl"
    # "12 expert 20 100 relx"
    # "12 expert 20 100 flax"
    # "15 expert 40 100 pure"
    # "15 expert 40 100 ploi"
    # "15 expert 40 100 cmpl"
    # "15 expert 40 100 relx"
    # "15 expert 40 100 flax"

    # "10 easy 5 300 pure"
    # "10 medium 5 200 ploi"
    # "10 hard 5 100 cmpl"
    # "12 easy 20 300 relx"
    # "12 medium 20 200 flax"
)

# Loop over each configuration and run the experiment.
for exp in "${experiments[@]}"; do
    # Split the configuration into variables.
    set -- $exp  # now $1=PROBLEM_SIZE, $2=DIFFICULTY, $3=TIMEOUT, $4=NUM_TEST_PROBLEMS, $5=PLANNER_TYPE
    run_experiment "$1" "$2" "$3" "$4" "$5"
done
