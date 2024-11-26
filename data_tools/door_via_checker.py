import json

# Load your JSON file (replace 'your_file.json' with your actual file name)
with open('data/sceneGraphs/new_structure/3dsg_full.json', 'r') as file:
    data = json.load(file)

# Step 1: List all door node IDs
door_ids = []
for component in data["nodes"]["components"]:
    if component["type"] == "door":
        door_ids.append(component["id"])

# Step 2: Collect all 'via' IDs from links
via_ids = {link["via"] for link in data["links"] if "via" in link}

# Step 3: Find door IDs not included in any link's "via"
missing_doors = [door_id for door_id in door_ids if door_id not in via_ids]

# Print the results
if missing_doors:
    print("The following door IDs are not included in any link's 'via':")
    print(missing_doors)
else:
    print("All door IDs are included in links' 'via'.")

#[5045, 5046, 5047, 5052, 5053, 5055, 5056, 5059, 5061, 5063, 5065, 5066, 5070] missing