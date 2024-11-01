import json

# Load the JSON file
with open('data/sceneGraphs/3D_Scene_Graph_Large_withCOR.json', 'r') as file:
    data = json.load(file)

# Function to filter nodes while keeping necessary attributes
def filter_space(space):
    return {
        "id": space["id"],
        "type": space["type"]
    }

def filter_element(element):
    return {
        "id": element["id"],
        "type": element["type"],
        "room": element.get("room")
    }

def filter_component(component):
    return {
        "id": component["id"],
        "type": component["type"],
        "room": component.get("room")
    }

def filter_link(link):
    return {
        "nodes": [link["source"], link["target"]],
        "width": link.get("width")
    }


# Apply filters to retain only the desired structure and attributes
filtered_data = {
    "spaces": [filter_space(space) for space in data.get("spaces", [])],
    "elements": [filter_element(element) for element in data.get("elements", [])],
    "components": [filter_component(component) for component in data.get("components", [])],
    "links": [filter_link(link) for link in data.get("links", [])]
}

# Save the filtered data to a new JSON file
with open('data/sceneGraphs/trimmed_3dsg.json', 'w') as outfile:
    json.dump(filtered_data, outfile, indent=4)

print("Filtered data saved to /mnt/data/trimmed_3dsg.json")
