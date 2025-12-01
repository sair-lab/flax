#!/bin/bash

export PYTHONPATH=$(pwd):$PYTHONPATH
DOMAIN_NAME="MazeNamo"

run_experiment() {
    local problem_size=$1
    local problem_mode=$2
    local problem_idx=$3
    local planner_type=$4
    local test_timeout=$5
    local test_planner_name=$6
    local train_planner_name=$7
    local guider_name=$8
    local seed=$9
    local cmpl_rules=${10}
    local relx_rules=${11}
    local vis_log_dir=${12:-vis}

    # Remove any existing "mazenamo_test"
    if [ -L "pddlgym/pddl/mazenamo_test" ]; then
        unlink "pddlgym/pddl/mazenamo_test"
    elif [ -d "pddlgym/pddl/mazenamo_test" ]; then
        rm -rf "pddlgym/pddl/mazenamo_test"
    fi

    # Determine the problem directory containing PDDL files.
    local problem_dir="$(pwd)/pddl_files/problems/mazenamo_problems/pddl_${problem_size}x${problem_size}_${problem_mode}"
    if [[ "$problem_idx" == "all" ]]; then
        # Link the entire problem directory to "mazenamo_test"
        ln -s "$problem_dir" pddlgym/pddl/mazenamo_test
    else
        # Create a new folder "mazenamo_test" inside pddlgym/pddl
        mkdir -p pddlgym/pddl/mazenamo_test

        # Find one PDDL file (the first one found) in that directory.
        local pddl_file
        pddl_file="${problem_dir}/namo_problem_${problem_idx}.pddl"
        if [ -z "$pddl_file" ]; then
            echo "No PDDL file found in $problem_dir. Skipping experiment."
            return
        fi

        # Create a symlink inside "mazenamo_test" pointing to the chosen PDDL file.
        ln -s "$pddl_file" pddlgym/pddl/mazenamo_test/
    fi

    # Build the Python command.
    # Required arguments are: --domain_name, --problem_size, --problem_mode, --problem_idx,
    # --test_planner_name, --guider_name, --seed, --planner_type, --test_timeout, and --vis_log_dir.
    # For non-"pure" planners, we add --train_planner_name, --cmpl_rules and --relx_rules.
    cmd="python -u src/minigrid_visualization.py --domain_name ${DOMAIN_NAME} \
        --problem_size ${problem_size} --problem_mode ${problem_mode} --problem_idx ${problem_idx} \
        --test_planner_name ${test_planner_name} --guider_name ${guider_name} --seed ${seed} \
        --planner_type ${planner_type} --test_timeout ${test_timeout} --vis_log_dir ${vis_log_dir}"
    if [ "$planner_type" != "pure" ]; then
         cmd+=" --train_planner_name ${train_planner_name} --cmpl_rules ${cmpl_rules} --relx_rules ${relx_rules}"
    fi

    echo "--------------------------------------------------"
    echo "Running experiment:"
    echo "  Problem: ${problem_size}x${problem_size} ${problem_mode} (index ${problem_idx})"
    echo "  Planner type: ${planner_type}"
    echo "  Command: ${cmd}"
    echo "--------------------------------------------------"
    eval $cmd

    # After the experiment, remove the temporary "mazenamo_test" folder.
    if [ -L "pddlgym/pddl/mazenamo_test" ]; then
        unlink "pddlgym/pddl/mazenamo_test"
    elif [ -d "pddlgym/pddl/mazenamo_test" ]; then
        rm -rf "pddlgym/pddl/mazenamo_test"
    fi
}

# List of experiments.
# Each experiment is specified as a space‐separated string with the following fields:
#   problem_size, problem_mode, problem_idx, planner_type, test_timeout,
#   test_planner_name, train_planner_name, guider_name, seed, cmpl_rules, relx_rules, vis_log_dir
# For "pure" planner type, leave train_planner_name, cmpl_rules and relx_rules as empty strings.
experiments=(
    # "10 hard all flax 5 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis"
    # "10 hard 7 pure 5 fd-lama-first '' no-guidance 0 '' '' vis --draw_scores"
    # "10 hard 7 ploi 5 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis --draw_scores"
    # "10 hard 7 flax 5 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis --draw_scores"
    # "12 hard 59 pure 20 fd-lama-first '' no-guidance 0 '' '' vis --draw_scores"
    # "12 hard 59 ploi 20 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis --draw_scores"
    # "12 hard 59 flax 20 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis --draw_scores"
    "15 hard 18 pure 40 fd-lama-first '' no-guidance 0 '' '' vis --draw_scores"
    "15 hard 18 ploi 40 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis --draw_scores"
    "15 hard 18 flax 40 fd-lama-first fd-opt-lmcut gnn-bce-10 8 config/mazenamo_complementary_rules.json config/mazenamo_relaxation_rules_1.json vis --draw_scores"
)

# Loop over each experiment.
for exp in "${experiments[@]}"; do
    read -r problem_size problem_mode problem_idx planner_type test_timeout test_planner_name train_planner_name guider_name seed cmpl_rules relx_rules vis_log_dir <<< "$exp"
    echo "Testing problem: size=${problem_size}, mode=${problem_mode}, index=${problem_idx}, planner=${planner_type}"
    run_experiment "$problem_size" "$problem_mode" "$problem_idx" "$planner_type" "$test_timeout" "$test_planner_name" "$train_planner_name" "$guider_name" "$seed" "$cmpl_rules" "$relx_rules" "$vis_log_dir"
done

echo "All experiments finished and temporary files cleaned up."
