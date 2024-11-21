import json
import re
from collections import defaultdict

# import os

# # 현재 작업 디렉토리 출력
# print("Current working directory:", os.getcwd())

# Load the original JSON data
with open('/Users/nayunkim/Documents/GitHub/repairPlan/data/graphs/BIM_COR/graphml_int_link.json', 'r') as file:
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

# First, define the pca_to_size function as provided
def pca_to_size(pca1, pca2, pca3, extent_pca1, extent_pca2, extent_pca3):
    size_x = (abs(pca1[0]) * extent_pca1 +
              abs(pca2[0]) * extent_pca2 +
              abs(pca3[0]) * extent_pca3)
    size_y = (abs(pca1[1]) * extent_pca1 +
              abs(pca2[1]) * extent_pca2 +
              abs(pca3[1]) * extent_pca3)
    size_z = (abs(pca1[2]) * extent_pca1 +
              abs(pca2[2]) * extent_pca2 +
              abs(pca3[2]) * extent_pca3)
    return size_x, size_y, size_z

# Update the node processing loop
for node in nodes:
    old_id = str(node['id'])
    node_type = node.get('node_type')
    label = node.get('label')
    new_id = None

    # Extract location
    location = [node.get('cp_x'), node.get('cp_y'), node.get('cp_z')]

    # Extract PCA values and compute size
    pca1 = [node.get('pca1x'), node.get('pca1y'), node.get('pca1z')]
    pca2 = [node.get('pca2x'), node.get('pca2y'), node.get('pca2z')]
    pca3 = [node.get('pca3x'), node.get('pca3y'), node.get('pca3z')]
    extent_pca1 = node.get('extent_pca1')
    extent_pca2 = node.get('extent_pca2')
    extent_pca3 = node.get('extent_pca3')
    size = pca_to_size(pca1, pca2, pca3, extent_pca1, extent_pca2, extent_pca3)

    if node_type == 'space':
        # Assign new ID to space
        new_id = space_id_counter
        space_id_counter += 1
        spaces_dict[old_id] = {
            'id': new_id,
            'surfaces': [],
            'location': location,
            'size': size
        }
    elif label == 1:
        # Wall surface
        new_id = wall_id_counter
        wall_id_counter += 1
        surfaces_dict[old_id] = {
            'id': new_id,
            'type': 'wall',
            'components': [],
            'location': location,
            'size': size
        }
    elif label == 2:
        # Floor surface
        new_id = floor_id_counter
        floor_id_counter += 1
        surfaces_dict[old_id] = {
            'id': new_id,
            'type': 'floor',
            'components': [],
            'location': location,
            'size': size
        }
    elif label == 3:
        # Ceiling surface
        new_id = ceiling_id_counter
        ceiling_id_counter += 1
        surfaces_dict[old_id] = {
            'id': new_id,
            'type': 'ceiling',
            'components': [],
            'location': location,
            'size': size
        }
    elif label == 4:
        # Door component
        new_id = door_id_counter
        door_id_counter += 1
        components_dict[old_id] = {
            'id': new_id,
            'type': 'door',
            'location': location,
            'size': size
        }
    elif label == 5:
        # Window component
        new_id = window_id_counter
        window_id_counter += 1
        components_dict[old_id] = {
            'id': new_id,
            'type': 'window',
            'location': location,
            'size': size
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

# Prepare the final hierarchical JSON structure with dimensions (full version)
output_json_full = {
    'nodes': {
        'spaces': list(spaces_dict.values()),
        'surfaces': list(surfaces_dict.values()),
        'components': list(components_dict.values())
    },
    'links': links_list
}

# Prepare the trimmed version without 'size' and 'location' (trimmed version)
import copy

# Function to remove 'size' and 'location' recursively
def remove_dimensions(data):
    if isinstance(data, list):
        return [remove_dimensions(item) for item in data]
    elif isinstance(data, dict):
        return {k: remove_dimensions(v) for k, v in data.items() if k not in ('size', 'location')}
    else:
        return data

# Create a deep copy to avoid modifying the original full data
output_json_trimmed = remove_dimensions(copy.deepcopy(output_json_full))

# Now you have both versions:   
# output_json_full includes 'size' and 'location'
# output_json_trimmed excludes 'size' and 'location'



# You can output or save both JSONs as needed
with open('data/sceneGraphs/new_structure/3dsg_full.json', 'w') as file:
    json.dump(output_json_full, file, indent=4)

with open('data/sceneGraphs/new_structure/3dsg_trimmed.json', 'w') as file:
    json.dump(output_json_trimmed, file, indent=4)
