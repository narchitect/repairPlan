import json
import csv
import math

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

# Label mapping
label_mapping = {
    1: 'Wall',
    2: 'Floor',
    3: 'Ceiling',
    4: 'Door',
    5: 'Window',
    6: 'Column',
    7: 'Stair',
    8: 'Pipe',
    9: 'Sink',
    10: 'Toilet',
    11: 'Sprinkler',
    12: 'Tank',
    13: 'Duct',
    14: 'AirTerminal',
    15: 'Light',
    16: 'Alarm',
    17: 'Sensor',
    18: 'Outlet',
    19: 'Switch',
    20: 'Table',
    21: 'Chair',
    22: 'Bookshelf',
    23: 'Appliance',
    24: 'Space',
    25: 'SpaceHeater',
    26: 'Proxy',
    999: 'Other'
}

# Categories
element_labels = {1, 2, 3}  # Wall, Floor, Ceiling
component_labels = {4, 5}   # Door, Window
space_label = 24            # Space

# Load the original JSON data
with open('../data/graphs/BIM_COR/graphml.json', 'r') as file:
    graphmlData = json.load(file)

# Load the pem.csv file and create a mapping
pem_data = {}
with open('../data/graphs/BIM_COR/pem.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        guid_int = row.get('guid_int', '').strip()
        pem_data[guid_int] = {
            'parent_element': row.get('parent_element', '').strip(),
            'ifc_guid': row.get('ifc_guid', '').strip()
        }

# Initialize dictionaries and lists
nodes_by_id = {}
spaces = []
elements = []
components = []

# Process each node
for node in graphmlData['nodes']:
    label = node['label']
    node_type = label_mapping.get(label, 'Other')

    # Compute sizes using PCA attributes
    pca1 = (node['pca1x'], node['pca1y'], node['pca1z'])
    pca2 = (node['pca2x'], node['pca2y'], node['pca2z'])
    pca3 = (node['pca3x'], node['pca3y'], node['pca3z'])
    extent_pca1 = node['extent_pca1']
    extent_pca2 = node['extent_pca2']
    extent_pca3 = node['extent_pca3']

    size_x, size_y, size_z = pca_to_size(
        pca1, pca2, pca3, extent_pca1, extent_pca2, extent_pca3)

    # Get the 'ifc_guid', and if it's NaN, replace it using pem_data
    ifc_guid = node.get('ifc_guid', '')

    if isinstance(ifc_guid, float) and math.isnan(ifc_guid):
        node_id = node.get('id', '')
        node_id_str = str(node_id).strip()
        if node_id_str in pem_data:
            # Get the parent_element(s) from pem_data
            parent_elements = pem_data[node_id_str].get('parent_element', '')
            # Remove square brackets if present
            parent_elements = parent_elements.strip('[]')
            # Split and strip the parent IDs
            parent_ids = [pid.strip() for pid in parent_elements.split(',') if pid.strip()]

            ifc_guids = []
            for parent_id in parent_ids:
                # Ensure parent_id is a string and strip any whitespace
                parent_id_str = str(parent_id).strip()
                # Convert parent_id_str to integer to remove decimal points
                try:
                    parent_id_int = int(float(parent_id_str))
                    parent_id_str = str(parent_id_int)
                except ValueError:
                    print(f"Invalid parent_id '{parent_id_str}' for node id: {node_id_str}")
                    continue  # Skip this parent_id if it cannot be converted

                parent_data = pem_data.get(parent_id_str)
                if parent_data:
                    parent_ifc_guid = parent_data.get('ifc_guid', '').strip()
                    if parent_ifc_guid:
                        ifc_guids.append(parent_ifc_guid)
                    else:
                        print(f"No ifc_guid in parent_data for parent_id: '{parent_id_str}'")
                else:
                    print(f"Parent data not found for parent_id: '{parent_id_str}'")
            if ifc_guids:
                # If multiple ifc_guids, decide how to handle them (e.g., join them)
                ifc_guid = ','.join(ifc_guids)
            else:
                ifc_guid = ''
                print(f"No ifc_guid found for parent elements of node id: {node_id_str}")
        else:
            ifc_guid = ''
            print(f"Node id {node_id_str} not found in pem.csv")

    # Prepare the new node
    new_node = {
        'id': int(node['id']),
        'ifc_guid': ifc_guid,
        'type': node_type,
        'location': {
            'x': node['cp_x'],
            'y': node['cp_y'],
            'z': node['cp_z']
        },
        'size': {
            'x': size_x,
            'y': size_y,
            'z': size_z
        }
    }

    # Add to nodes_by_id
    nodes_by_id[new_node['id']] = new_node

    if label == space_label:
        # This is a space node
        space = new_node.copy()
        # Initialize 'contain_nodes' with 'elements' and 'components' keys
        space['contain_nodes'] = {'elements': [], 'components': []}
        spaces.append(space)
    elif label in element_labels:
        # This is an element (structure)
        # Assign the room(s) based on the 'room' attribute
        room = node.get('room', '')
        new_node['room'] = room.strip('[]')  # Remove brackets if present
        elements.append(new_node)
    elif label in component_labels:
        # This is a component
        # Assign the room(s) based on the 'room' attribute
        room = node.get('room', '')
        new_node['room'] = room.strip('[]')  # Remove brackets if present
        components.append(new_node)
    else:
        # Other labels can be processed as needed
        pass

# Create a mapping from space IDs to space nodes
spaces_by_id = {str(space['id']): space for space in spaces}

# Assign elements to spaces
for element in elements:
    room_str = element.get('room', '')
    room_ids = [r.strip() for r in room_str.split(',') if r.strip()]
    for room_id in room_ids:
        space = spaces_by_id.get(room_id)
        if space:
            space['contain_nodes']['elements'].append(element['id'])
        else:
            print(f"Space with id {room_id} not found for element id {element['id']}")

# Assign components to spaces
for component in components:
    room_str = component.get('room', '')
    room_ids = [r.strip() for r in room_str.split(',') if r.strip()]
    for room_id in room_ids:
        space = spaces_by_id.get(room_id)
        if space:
            space['contain_nodes']['components'].append(component['id'])
        else:
            print(f"Space with id {room_id} not found for component id {component['id']}")

# Process links from the original JSON
links = []
if 'links' in graphmlData:
    for link in graphmlData['links']:
        node1 = link.get('source')
        node2 = link.get('target')
        width = link.get('width')
        if node1 and node2 and width is not None:
            links.append({
                "nodes": [node1, node2],
                "width": width
            })

# Create the new JSON structure
new_data = {
    'spaces': spaces,
    'elements': elements,
    'components': components,
    'links': links
}

# Save the new JSON file
with open('../data/sceneGraphs/new3dsg.json', 'w') as file:
    json.dump(new_data, file, indent=4)

print("New JSON file 'new3dsg.json' has been created with spaces, elements, components, and links.")
