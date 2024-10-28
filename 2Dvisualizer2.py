import json
import networkx as nx
from pyvis.network import Network

import pyvis


print(pyvis.__file__)

def load_scene_graph(filepath):
    """
    Loads the scene graph from a JSON file.

    Args:
        filepath (str): Path to the JSON file containing the scene graph.

    Returns:
        dict: Parsed JSON data.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


# Load the scene graph data
data = load_scene_graph("data/3D_Scene_Graph_large.json")

# Create a new graph
G = nx.Graph()

# Add spaces as nodes
for space in data.get('spaces', []):
    G.add_node(space['id'], type='space', label=space['id'])

# Add components as nodes and connect them to their spaces
for component in data.get('components', []):
    G.add_node(component['id'], type=component['type'], label=component['id'])
    G.add_edge(component['id'], component['room'], relationship='belongs_to')

# Add elements as nodes and connect them to their spaces
for element in data.get('elements', []):
    G.add_node(element['id'], type=element['type'], label=element['id'])
    G.add_edge(element['id'], element['room'], relationship='belongs_to')

# Add additional links
for link in data.get('links', []):
    if len(link) >= 2:
        source, target = link[:2]
        G.add_edge(source, target, relationship='linked_to')

# Define node colors based on their type
color_map = {
    'space': '#1f78b4',  # Blue
    'wall': '#8c564b',  # Brown
    'ceiling': '#e377c2',  # Pink
    'floor': '#7f7f7f',  # Gray
    'door': '#ff7f0e',  # Orange
    'window': '#2ca02c',  # Green
    'unknown': '#d3d3d3'  # Light Gray for undefined types
}

# Initialize PyVis Network
net = Network(height='1800px', width='100%', bgcolor='#222222', font_color='white')

# Add nodes with custom styles
for node, attrs in G.nodes(data=True):
    node_type = attrs.get('type', 'unknown')
    color = color_map.get(node_type, color_map['unknown'])

    # Tooltip title
    title = f"Type: {node_type.capitalize()}<br>ID: {node}"

    net.add_node(
        node,
        label=node,
        title=title,
        color=color,
        shape='box' if node_type == 'space' else 'ellipse'
    )

# Add edges with custom styles
for source, target, attrs in G.edges(data=True):
    relationship = attrs.get('relationship', 'unknown')

    if relationship == 'belongs_to':
        color = '#ffffff'  # White
        width = 1
        style = 'solid'
    elif relationship == 'linked_to':
        color = '#ffff00'  # Yellow
        width = 2
        style = 'dashed'
    else:
        color = '#808080'  # Gray
        width = 1
        style = 'dotted'

    net.add_edge(
        source,
        target,
        title=relationship,
        color=color,
        width=width
    )





# # Configure the physics layout for better visualization
# net.force_atlas_2based(
#     gravity=-50,              # Corrected parameter name
#     central_gravity=0.01,
#     spring_length=100,
#     spring_strength=0.08,
#     damping=0.4
# )


# Generate the interactive network and save as HTML

net.show('scene_graph.html', notebook=False)
