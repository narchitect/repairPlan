import networkx as nx
import json

# Replace 'input.graphml' with the path to your GraphML file
graphml_file = '/Users/nayunkim/Documents/GitHub/thesis/data/graphs/output_modifiedCOR/bim_room_graph.graphml'
# Replace 'output.json' with the desired output JSON file name
json_file = '../data/graphs/BIM_COR/graphml_int.json'

# Read the GraphML file
G = nx.read_graphml(graphml_file)

# Convert the graph to a node-link format data dictionary
data = nx.node_link_data(G)

# Write the data to a JSON file
with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)
