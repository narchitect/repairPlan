import json
import re
from data.robots import actions, equipments, materials, robots

def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph

def extract_json(response_content):
    # Extract the JSON part from the response using regex
    json_match = re.search(r'```json\n(.*?)\n```', response_content, re.DOTALL)
    if json_match:
        json_output = json_match.group(1)
        try:
            return json.loads(json_output)  # Parse and return the JSON content
        except json.JSONDecodeError:
            print("An error occurred while parsing the json response")
            return None
    else:
        print("Can't find the JSON output section")
        return None

# Global full scene graph 
SCENE_GRAPH_PATH = "/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/new_structure/3dsg_full_fixed_doors.json"
GLOBAL_SCENE_GRAPH = load_scene_graph(SCENE_GRAPH_PATH)

def get_node_info(node_id: int) -> str:
    full_graph = GLOBAL_SCENE_GRAPH.get('nodes', {})

    # flatten
    all_nodes = [
        node for key in full_graph
        for node in full_graph.get(key, []) if isinstance(full_graph[key], list)
    ]

    # find the node with the matching id
    result = next((node for node in all_nodes if node["id"] == node_id), None)

    # convert the result to a string
    result_dict = result if result else {"error": f"Node {node_id} not found"}
    return result_dict

def get_room_id_by_node_id(node_id):
    nodes = GLOBAL_SCENE_GRAPH["nodes"]
    # Build sets of IDs for quick lookup
    space_ids = set(space["id"] for space in nodes["spaces"])
    surface_ids = set(surface["id"] for surface in nodes["surfaces"])
    component_ids = set(component["id"] for component in nodes["components"])
    
    # Build a mapping from surface ID to space ID
    surface_to_space = {}
    for space in nodes["spaces"]:
        space_id = space["id"]
        for surface_id in space["surfaces"]:
            surface_to_space[surface_id] = space_id

    # Build a mapping from component ID to surface ID
    component_to_surface = {}
    for surface in nodes["surfaces"]:
        surface_id = surface["id"]
        for component_id in surface["components"]:
            component_to_surface[component_id] = surface_id

    # Determine the space ID based on the node ID type
    if node_id in space_ids:
        # The node is a space
        return node_id
    elif node_id in surface_ids:
        # The node is a surface
        space_id = surface_to_space.get(node_id)
        return space_id
    elif node_id in component_ids:
        # The node is a component
        surface_id = component_to_surface.get(node_id)
        space_id = surface_to_space.get(surface_id)
        return space_id
    else:
        # Node ID not found
        print(f"Node ID {node_id} not found in spaces, surfaces, or components.")
        return None

def get_room_infos(node_id):
    scene_graph = GLOBAL_SCENE_GRAPH.get('nodes', {})
    # Build lookup dictionaries for quick access
    id_to_node = {
        'spaces': {node['id']: node for node in scene_graph.get('spaces', [])},
        'surfaces': {node['id']: node for node in scene_graph.get('surfaces', [])},
        'components': {node['id']: node for node in scene_graph.get('components', [])}
    }

    # Initialize result lists
    associated_spaces = []
    associated_nodes = []

    # Find the input node in 'surfaces' or 'components'
    node = id_to_node['surfaces'].get(node_id) or id_to_node['components'].get(node_id)
    if not node:
        return {'error': f'Node ID {node_id} not found in surfaces or components.'}

    associated_space_ids = set()

    if node_id in id_to_node['surfaces']:
        # Node is a surface
        # Find all spaces that include this surface
        for space in scene_graph.get('spaces', []):
            if node_id in space.get('surfaces', []):
                associated_spaces.append(space)
                associated_space_ids.add(space['id'])
    elif node_id in id_to_node['components']:
        # Node is a component
        # Find all surfaces that include this component
        associated_surface_ids = []
        for surface in scene_graph.get('surfaces', []):
            if node_id in surface.get('components', []):
                associated_surface_ids.append(surface['id'])
                # For each surface, find spaces that include this surface
                for space in scene_graph.get('spaces', []):
                    if surface['id'] in space.get('surfaces', []):
                        associated_spaces.append(space)
                        associated_space_ids.add(space['id'])
    else:
        # Node is neither surface nor component
        return {'error': f'Node ID {node_id} is neither surface nor component.'}

    # If the defect_node is a surface, add its components to associated_nodes
    if node_id in id_to_node['surfaces']:
        for component_id in node.get('components', []):
            component_node = id_to_node['components'].get(component_id)
            if component_node:
                associated_nodes.append(component_node)

    # Now collect all nodes that are associated with the same spaces
    # Collect associated surfaces and components
    for space_id in associated_space_ids:
        space_node = id_to_node['spaces'][space_id]
        # Add surfaces
        for surface_id in space_node.get('surfaces', []):
            surface_node = id_to_node['surfaces'].get(surface_id)
            if surface_node and surface_node['id'] != node_id:
                associated_nodes.append(surface_node)
            # For each surface, also add components
            for component_id in surface_node.get('components', []):
                component_node = id_to_node['components'].get(component_id)
                if component_node and component_node['id'] != node_id:
                    associated_nodes.append(component_node)
    
    # if the defect_node is a component, add itselt to the associated_nodes
    if node_id in id_to_node['components']:
        associated_nodes.append(node)


    # Remove duplicates
    associated_nodes = list({n['id']: n for n in associated_nodes}.values())
    associated_spaces = list({s['id']: s for s in associated_spaces}.values())

    # Prepare the result
    result = {
        "defect_node": node,
        "associated_spaces": associated_spaces,
        "associated_nodes": associated_nodes
    }

    return result



def get_robot_info_by_id(robot_id):
    selected_robot = next((robot for robot in robots if robot['id'] == robot_id), None)

    result = {
        "robot_configs": {
            "actions": actions,
            "equipments": equipments,
            "materials": materials,
        },
        "robots": selected_robot
    }
    return result

if __name__ == "__main__":
    print(get_node_info(1004))