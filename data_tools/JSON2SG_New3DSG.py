import json
import re
from collections import defaultdict

# Load the original JSON data
with open('../data/graphs/BIM_COR/graphml_int_link.json', 'r') as file:
    input_json = json.load(file)

# Load input data (replace with actual file reading if necessary)
nodes = input_json['nodes']
links = input_json['links']

label_mapping = {
    1: 'Wall',
    2: 'Floor',
    3: 'Ceiling',
    4: 'Door',
    5: 'Window',
    24: 'Space'
}

# Initialize counters for new IDs
space_id_counter = 0
wall_id_counter = 1000
ceiling_id_counter = 2000
floor_id_counter = 3000
window_id_counter = 4000
door_id_counter = 5000

# Mappings from old IDs to new IDs and nodes
old_id_to_new_id = {}
old_id_to_node = {}

# Dictionaries to hold the structured data
spaces_dict = {}
surfaces_dict = {}
components_dict = {}
links_list = []

# First, process all nodes to assign new IDs and categorize them
for node in nodes:
    old_id = str(node['id'])
    node_type = node.get('node_type')
    label = node.get('label')
    new_id = None

    if node_type == 'space':
        # Assign new ID to space
        new_id = space_id_counter
        space_id_counter += 1
        spaces_dict[old_id] = {
            'id': new_id,
            'surfaces': []
        }
    elif label == 1:
        # Wall surface
        new_id = wall_id_counter
        wall_id_counter += 1
        surfaces_dict[old_id] = {
            'id': new_id,
            'type': 'wall',
            'components': []
        }
    elif label == 2:
        # Floor surface
        new_id = floor_id_counter
        floor_id_counter += 1
        surfaces_dict[old_id] = {
            'id': new_id,
            'type': 'floor',
            'components': []
        }
    elif label == 3:
        # Ceiling surface
        new_id = ceiling_id_counter
        ceiling_id_counter += 1
        surfaces_dict[old_id] = {
            'id': new_id,
            'type': 'ceiling',
            'components': []
        }
    elif label == 4:
        # Door component
        new_id = door_id_counter
        door_id_counter += 1
        components_dict[old_id] = {
            'id': new_id,
            'type': 'door'
        }
    elif label == 5:
        # Window component
        new_id = window_id_counter
        window_id_counter += 1
        components_dict[old_id] = {
            'id': new_id,
            'type': 'window'
        }

    if new_id is not None:
        old_id_to_new_id[old_id] = new_id
        old_id_to_node[old_id] = node

# Assign surfaces to spaces based on the 'room' attribute
for old_id, surface in surfaces_dict.items():
    node = old_id_to_node[old_id]
    room = node.get('room')
    if room:
        # Extract space IDs from the 'room' string
        space_ids = re.findall(r'\d+', room)
        for space_id in space_ids:
            if space_id in spaces_dict:
                spaces_dict[space_id]['surfaces'].append(surface['id'])

# Assign components to surfaces based on links
for link in links:
    source_old_id = str(link['source'])
    target_old_id = str(link['target'])

    # Check if source is a component and target is a surface
    if source_old_id in components_dict and target_old_id in surfaces_dict:
        component = components_dict[source_old_id]
        surface = surfaces_dict[target_old_id]
        surface['components'].append(component['id'])
    # Check if target is a component and source is a surface
    elif target_old_id in components_dict and source_old_id in surfaces_dict:
        component = components_dict[target_old_id]
        surface = surfaces_dict[source_old_id]
        surface['components'].append(component['id'])

# Create links between spaces via doors
door_to_spaces = defaultdict(set)

for link in links:
    source_old_id = str(link['source'])
    target_old_id = str(link['target'])

    # Check if source is a door and target is a space
    if source_old_id in components_dict and components_dict[source_old_id]['type'] == 'door' and target_old_id in spaces_dict:
        door_id = components_dict[source_old_id]['id']
        space_id = spaces_dict[target_old_id]['id']
        door_to_spaces[door_id].add(space_id)
    # Check if target is a door and source is a space
    elif target_old_id in components_dict and components_dict[target_old_id]['type'] == 'door' and source_old_id in spaces_dict:
        door_id = components_dict[target_old_id]['id']
        space_id = spaces_dict[source_old_id]['id']
        door_to_spaces[door_id].add(space_id)

# Now, create links between spaces via doors
for door_id, space_ids in door_to_spaces.items():
    if len(space_ids) == 2:
        space_list = list(space_ids)
        links_list.append({
            'spaces': space_list,
            'via': door_id
        })

# Prepare the final hierarchical JSON structure
output_json = {
    'spaces': list(spaces_dict.values()),
    'surfaces': list(surfaces_dict.values()),
    'components': list(components_dict.values()),
    'links': links_list
}

# Output the JSON (you can write it to a file if needed)


with open('../data/sceneGraphs/3dsg_new.json', 'w') as file:
    json.dump(output_json, file, indent=4)
