import json
import csv
import math

def pca_to_size(pca1, pca2, pca3, extent_pca1, extent_pca2, extent_pca3):
    """
    Convert PCA attributes to size along x, y, and z axes.

    Parameters:
    - pca1: Tuple or list of PCA1 components (pca1x, pca1y, pca1z).
    - pca2: Tuple or list of PCA2 components (pca2x, pca2y, pca2z).
    - pca3: Tuple or list of PCA3 components (pca3x, pca3y, pca3z).
    - extent_pca1: Extent along the first principal component.
    - extent_pca2: Extent along the second principal component.
    - extent_pca3: Extent along the third principal component.

    Returns:
    - A tuple (size_x, size_y, size_z) representing the size along each axis.
    """
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
    999: 'Roof'  # Assuming label 999 corresponds to 'Roof'
    # Add other labels if necessary
}

# Categories
element_labels = {1, 2, 3, 999}  # Wall, Floor, Ceiling, Roof
component_labels = {4, 5}        # Door, Window
space_label = 24                 # Space

# Load the original JSON data
with open('output.json', 'r') as file:
    data = json.load(file)

# Load the pem.csv file and create a mapping from guid_int to match_id
pem_mapping = {}
with open('pem.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        guid_int = row.get('guid_int')
        match_id = row.get('match_id')
        if guid_int and match_id:
            pem_mapping[guid_int] = match_id

# Lists to hold spaces, elements, and components
spaces = []
elements = []
components = []

# Process each node
for node in data['nodes']:
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

    # Get the 'ifc_guid', and if it's missing or 'NaN', replace it using pem_mapping
    ifc_guid = node.get('ifc_guid', '')
    if not ifc_guid or (isinstance(ifc_guid, float) and math.isnan(ifc_guid)):
        node_id = node.get('id', '')
        # The 'id' in the node corresponds to 'guid_int' in pem.csv
        node_id_str = str(node_id)
        if node_id_str in pem_mapping:
            ifc_guid = pem_mapping[node_id_str]
        else:
            ifc_guid = ''  # If not found, leave it empty or handle as needed
            print(f"ifc_guid not found for node id: {node_id_str}")

    # Prepare the new node
    new_node = {
        'id': node['id'],
        'ifc_guid': ifc_guid,
        'type': node_type,
        'size': {
            'x': size_x,
            'y': size_y,
            'z': size_z
        }
    }

    if label == space_label:
        # This is a space node
        space = new_node.copy()
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

# Process links from the original JSON
links = []
if 'links' in data:
    for link in data['links']:
        source = link.get('source')
        target = link.get('target')
        if source and target:
            links.append([source, target])

# Create the new JSON structure
new_data = {
    'spaces': spaces,
    'elements': elements,
    'components': components,
    'links': links  # Add the links here
}

# Save the new JSON file
with open('new_structure.json', 'w') as file:
    json.dump(new_data, file, indent=4)

print("New JSON file 'new_structure.json' has been created with spaces, elements, components, and links.")
