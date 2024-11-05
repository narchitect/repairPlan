import json
import matplotlib.pyplot as plt

# Load the JSON data
with open('../data/sceneGraphs/3dsg_withCOR.json', 'r') as f:
    data = json.load(f)

# Print top-level keys
print(data.keys())

# Dictionary to store node positions
node_positions = {}

# Function to extract positions from items
def extract_positions(items):
    for item in items:
        node_id = item['id']
        # Assuming 'position' field exists with 'x', 'y', 'z' coordinates
        position = item.get('position') or item.get('size')  # Use 'size' if 'position' is not available
        if position:
            x = position.get('x', 0)
            y = position.get('y', 0)
            z = position.get('z', 0)
            node_positions[node_id] = (x, y, z)

# Extract positions from 'spaces', 'elements', and 'components'
extract_positions(data.get('spaces', []))
extract_positions(data.get('elements', []))
extract_positions(data.get('components', []))

# Extract links
links = data.get('links', [])

# Function to plot the nodes and links
def plot_building_plan(highlight_nodes=None):
    if highlight_nodes is None:
        highlight_nodes = []

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot all nodes
    for node_id, (x, y, _) in node_positions.items():
        ax.scatter(x, y, color='blue')
        ax.text(x, y, node_id, fontsize=9, ha='right')

    # Plot all links
    for link in links:
        # Adjust the keys here based on your data
        id1 = link.get('source')
        id2 = link.get('target')
        if id1 and id2 and id1 in node_positions and id2 in node_positions:
            x1, y1, _ = node_positions[id1]
            x2, y2, _ = node_positions[id2]
            ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1)

    # Highlight specified nodes
    for node_id in highlight_nodes:
        if node_id in node_positions:
            x, y, _ = node_positions[node_id]
            ax.scatter(x, y, color='red', s=100)
            ax.text(x, y, node_id, fontsize=9, ha='right', color='red')

    # Highlight links between specified nodes
    highlight_set = set(highlight_nodes)
    for link in links:
        id1 = link.get('source')
        id2 = link.get('target')
        if id1 and id2 and highlight_set.issuperset({id1, id2}):
            if id1 in node_positions and id2 in node_positions:
                x1, y1, _ = node_positions[id1]
                x2, y2, _ = node_positions[id2]
                ax.plot([x1, x2], [y1, y2], color='red', linewidth=2)

    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('Building Plan Visualization')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

# Example usage
highlight_nodes = ['14', '736']  # Replace with your list of node IDs
plot_building_plan(highlight_nodes)
