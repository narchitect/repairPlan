import json
from data.robots import actions, equipments, materials, robots

def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph

# Global full scene graph 
SCENE_GRAPH_PATH = "/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/new_structure/3dsg_full.json"
GLOBAL_SCENE_GRAPH = load_scene_graph(SCENE_GRAPH_PATH)

def get_node_info(node_id: int) -> str:
    full_graph = GLOBAL_SCENE_GRAPH

    # flatten
    all_nodes = [
        node for key in full_graph if key != 'links'
        for node in full_graph.get(key, []) if isinstance(full_graph[key], list)
    ]

    # find the node with the matching id
    result = next((node for node in all_nodes if node["id"] == node_id), None)

    # convert the result to a string
    result_dict = result if result else {"error": f"Node {node_id} not found"}
    return result_dict

def get_rooms_info(node_id):
    scene_graph = GLOBAL_SCENE_GRAPH
    # Build lookup dictionaries for quick access
    id_to_node = {
        'spaces': {node['id']: node for node in scene_graph.get('spaces', [])},
        'surfaces': {node['id']: node for node in scene_graph.get('surfaces', [])},
        'components': {node['id']: node for node in scene_graph.get('components', [])}
    }

    # Initialize result lists
    associated_spaces = []
    associated_nodes = []

    # Find the input node in 'elements' or 'components'
    node = id_to_node['surfaces'].get(node_id) or id_to_node['components'].get(node_id)
    if not node:
        return json.dumps({'error': f'Node ID {node_id} not found in surfaces or components.'})

    # Get room IDs associated with the node
    room_value = node.get('room', '')
    room_ids = [rid.strip() for rid in room_value.split(',') if rid.strip()]

    # Retrieve associated space nodes
    for rid in room_ids:
        space_node = id_to_node['spaces'].get(rid)
        if space_node:
            associated_spaces.append(space_node)

    # Collect all nodes that have the same room IDs
    for category in ['surfaces', 'components']:
        for n in scene_graph.get(category, []):
            n_room_value = n.get('room', '')
            n_room_ids = [rid.strip() for rid in n_room_value.split(',') if rid.strip()]
            if set(room_ids) & set(n_room_ids):
                associated_nodes.append(n)

    # Prepare the result
    result = {
        "defect_node": node,
        "associated_spaces": associated_spaces,
        "associated_surfaces": associated_nodes
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

