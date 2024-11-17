import json


def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph


def get_node_by_id(node_id: int, scene_graph) -> str:
    full_graph = scene_graph

    # flatten
    all_nodes = [
        node for key in full_graph if key != 'links'
        for node in full_graph.get(key, []) if isinstance(full_graph[key], list)
    ]

    # find the node with the matching id
    result = next((node for node in all_nodes if node["id"] == node_id), None)

    # convert the result to a string
    result_dict = result if result else {"error": f"Node {node_id} not found"}
    return json.dumps(result_dict)
