#!/bin/bash

CURRENT_DIR=$(pwd)
MINIGRID_REPO_URL="https://github.com/Farama-Foundation/Minigrid.git"
MINIGRID_REPO_DIR="Minigrid"
CONSTANTS_FILE="Minigrid/minigrid/core/constants.py"
WORLD_OBJECT_FILE="Minigrid/minigrid/core/world_object.py"
ENV_INIT_FILE="Minigrid/minigrid/envs/__init__.py"
INIT_FILE="Minigrid/minigrid/__init__.py"
TEMP_FILE="tmp.py"

# Clone the repository if it doesn't already exist
if [ ! -d "$MINIGRID_REPO_DIR" ]; then
    git clone "$MINIGRID_REPO_URL"
else
    echo "Minigrid repo already cloned."
fi

# Create symbolic links for new files
ln -s "$CURRENT_DIR/minigrid_mazenamo_env_patch/grid_3d.py" Minigrid/minigrid/core/grid_3d.py
ln -s "$CURRENT_DIR/minigrid_mazenamo_env_patch/mazenamo.py" Minigrid/minigrid/envs/mazenamo.py

# Modify `OBJECT_TO_IDX` dictionary (add two box types)
awk '
/^OBJECT_TO_IDX/ { in_object_to_idx=1 }  # Detect start of OBJECT_TO_IDX
in_object_to_idx && /^\}/ {              # Find the closing brace of OBJECT_TO_IDX
    print "    \"moveable_heavy_box\": 11,"
    print "    \"moveable_light_box\": 12,"
    in_object_to_idx=0
}
{ print }' "$CONSTANTS_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$CONSTANTS_FILE"


# Append the new class definitions to world_object.py (if not already present)
if ! grep -q "class MoveableHeavyBox(WorldObj):" "$WORLD_OBJECT_FILE"; then
    cat <<EOL >> "$WORLD_OBJECT_FILE"

class MoveableHeavyBox(WorldObj):
    def __init__(self, color):
        super().__init__("moveable_heavy_box", color)

    def can_pickup(self):
        return False

    def render(self, img):
        c = COLORS[self.color]

        # Outline
        fill_coords(img, point_in_rect(0.12, 0.88, 0.12, 0.88), c)
        fill_coords(img, point_in_rect(0.18, 0.82, 0.18, 0.82), (0, 0, 0))

        # Horizontal slit
        fill_coords(img, point_in_rect(0.16, 0.84, 0.47, 0.53), c)
    
    def see_behind(self) -> bool:
        return True

class MoveableLightBox(WorldObj):
    def __init__(self, color):
        super().__init__("moveable_light_box", color)

    def can_pickup(self):
        return True

    def render(self, img):
        c = COLORS[self.color]

        # Outline
        fill_coords(img, point_in_rect(0.12, 0.88, 0.12, 0.88), c)
        fill_coords(img, point_in_rect(0.18, 0.82, 0.18, 0.82), (0, 0, 0))

        # Horizontal slit
        fill_coords(img, point_in_rect(0.16, 0.84, 0.47, 0.53), c)

    def see_behind(self) -> bool:
        return True
EOL
else
    echo "Classes already exist in $WORLD_OBJECT_FILE, skipping append."
fi


# Append import statement to envs/__init__.py (if not already present)
if ! grep -q "from minigrid.envs.mazenamo import MazeNamoEnv" "$ENV_INIT_FILE"; then
    echo -e "\nfrom minigrid.envs.mazenamo import MazeNamoEnv" >> "$ENV_INIT_FILE"
else
    echo "Import statement already exists in $ENV_INIT_FILE, skipping."
fi


# Register MazeNAMO env in minigrid/__init__.py
awk '
/^def register_minigrid_envs\(\):/ { in_func=1 } {
    print
    if (in_func && $0 !~ /^[[:space:]]/ && NR > 1) {
        print "    # MazeNamo";
        print "    # ----------------------------------------";
        print "    register(";
        print "        id=\"MiniGrid-MazeNamo-v0\",";
        print "        entry_point=\"minigrid.envs:MazeNamoEnv\",";
        print "    )\n";
        in_func = 0
    }
}
' "$INIT_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$INIT_FILE"


cd Minigrid && pip install -e . && cd ..

echo "Add MazeNamo env to Minigrid successfully."
