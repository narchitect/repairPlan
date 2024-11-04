import networkx as nx
from pyvis.network import Network
from planner.planner import load_scene_graph

data = load_scene_graph("data/scene_graph_final.json")

# Create a new graph
G = nx.Graph()

# Add rooms as nodes
for room in data['room']:
    G.add_node(room['id'], type='room')

# Add objects as nodes and connect them to their rooms
for obj in data['object']:
    G.add_node(obj['id'], type='object')
    G.add_edge(obj['id'], obj['room'], relationship='belongs_to')

# Add assets as nodes and connect them to their rooms
for asset in data['asset']:
    # Extract the subtype from the asset's id
    subtype = asset['id'].split('_')[0].lower()

    G.add_node(
        asset['id'],
        type='asset',
        subtype=subtype,
        state=asset['state'],
        affordances=asset['affordances']
    )
    G.add_edge(asset['id'], asset['room'], relationship='belongs_to')

# Add additional links
for link in data['links']:
    source, target = link
    G.add_edge(source, target, relationship='linked_to')

# Define node colors based on their type or subtype
color_map = {
    'room': '#1f78b4',  # Blue
    'object': '#33a02c',  # Green
    'window': '#00FFFF',  # Cyan
    'door': '#FFA500',  # Orange
    'asset': '#e31a1c'  # Red for other assets
}

# Initialize PyVis Network
net = Network(height='1800px', width='100%', bgcolor='#222222', font_color='white')

# Add nodes with custom styles
for node, attrs in G.nodes(data=True):
    node_type = attrs.get('type', 'unknown')
    node_subtype = attrs.get('subtype', '').lower()

    # Determine the color
    if node_type == 'asset' and node_subtype in ['window', 'door']:
        color = color_map.get(node_subtype, 'gray')
    else:
        color = color_map.get(node_type, 'gray')

    title = f"{node_type.capitalize()}: {node}"
    net.add_node(node, label=node, title=title, color=color)

# Add edges with custom styles
for source, target, attrs in G.edges(data=True):
    relationship = attrs.get('relationship', 'unknown')
    if relationship == 'belongs_to':
        color = 'white'
        width = 1
    elif relationship == 'linked_to':
        color = 'yellow'
        width = 2
    else:
        color = 'gray'
        width = 0.5
    net.add_edge(source, target, title=relationship, color=color, width=width)

# Generate the interactive network
net.show('scene_graph.html', notebook=False)
