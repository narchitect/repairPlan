import json
import networkx as nx
from pyvis.network import Network
from planner.planner import load_scene_graph

# Load scene graph data
data = load_scene_graph("../data/sceneGraphs/3dsg_withCOR.json")

# Create a new graph
G = nx.Graph()

# Extract space nodes and their coordinates
for space in data['spaces']:
    x, y = space['location']['x'], space['location']['y']
    G.add_node(space['id'], type='space', pos=(x, y))

# Initialize PyVis Network
net = Network(height='1200px', width='100%', bgcolor='#222222', font_color='white')

# Add nodes with fixed positions
for node, attrs in G.nodes(data=True):
    if attrs.get('type') == 'space':
        x, y = attrs['pos']
        # pyvis expects x and y in a different range (px), so scale if needed
        net.add_node(node, label=node, title=f"Space ID: {node}", color='#1f78b4', x=x*10, y=-y*10, size= 5)

# Generate the interactive network with fixed positions
net.toggle_physics(False)


net.show('space_nodes.html', notebook=False)
