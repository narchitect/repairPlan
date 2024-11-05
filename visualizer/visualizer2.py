import json
import networkx as nx
import plotly.graph_objects as go

# Load the data from the JSON file
with open('../data/sceneGraphs/3dsg_withCOR.json', 'r') as f:
    data = json.load(f)

# Define node colors for each category and type
category_type_colors = {
    'spaces': 'blue',  # All spaces are blue
    'components': {
        'window': 'cyan',
        'door': 'orange'
    },
    'elements': {
        'ceiling': 'purple',
        'floor': 'brown',
        'wall': 'green'
    }
}

# Extract nodes and positions with category and type-specific colors
nodes = {}
node_colors = []
for category in ['spaces', 'elements', 'components']:
    for item in data.get(category, []):
        node_id = item['id']
        # Assuming each item has a 'position' field
        position = item.get('location', {'x': 0, 'y': 0, 'z': 0})
        nodes[node_id] = position

        # Determine color based on category and type
        if category == 'spaces':
            color = category_type_colors[category]
        else:
            item_type = item.get('type', '').lower()
            color = category_type_colors[category].get(item_type, 'gray')  # Default to gray if type is unrecognized
        node_colors.append(color)

# Build the graph
G = nx.Graph()
for node_id, position in nodes.items():
    G.add_node(node_id, pos=(position['x'], position['y'], position['z']))

# Add edges from links
for link in data.get('links', []):
    source = link.get('source')
    target = link.get('target')
    if source and target:
        G.add_edge(source, target)

# Get node positions
pos = nx.get_node_attributes(G, 'pos')

# Prepare node coordinates for Plotly
x_nodes = [pos[node][0] for node in G.nodes()]
y_nodes = [pos[node][1] for node in G.nodes()]
z_nodes = [pos[node][2] for node in G.nodes()]

# Prepare edge coordinates for Plotly
edge_x = []
edge_y = []
edge_z = []
for edge in G.edges():
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_z.extend([z0, z1, None])

# Create edge trace
edge_trace = go.Scatter3d(
    x=edge_x, y=edge_y, z=edge_z,
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines')

# Create node trace with category and type-specific colors
node_trace = go.Scatter3d(
    x=x_nodes, y=y_nodes, z=z_nodes,
    mode='markers',
    marker=dict(size=5, color=node_colors),
    hoverinfo='text',
    text=[f'Node {node_id}' for node_id in G.nodes()])

# List of node IDs to highlight
highlighted_nodes = ['14', '736']  # Replace with your node IDs

# Highlight edges connected to highlighted nodes
highlighted_edges = [
    edge for edge in G.edges()
    if edge[0] in highlighted_nodes or edge[1] in highlighted_nodes
]

highlighted_edge_x = []
highlighted_edge_y = []
highlighted_edge_z = []
for edge in highlighted_edges:
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    highlighted_edge_x.extend([x0, x1, None])
    highlighted_edge_y.extend([y0, y1, None])
    highlighted_edge_z.extend([z0, z1, None])

highlighted_edge_trace = go.Scatter3d(
    x=highlighted_edge_x, y=highlighted_edge_y, z=highlighted_edge_z,
    line=dict(width=3, color='red'),
    hoverinfo='none',
    mode='lines')

# Create the figure
fig = go.Figure(data=[edge_trace, highlighted_edge_trace, node_trace])

# Set the layout
fig.update_layout(
    scene=dict(
        xaxis=dict(title='X', showbackground=False),
        yaxis=dict(title='Y', showbackground=False),
        zaxis=dict(title='Z', showbackground=False)
    ),
    showlegend=False
)

# Show the figure
fig.show()
