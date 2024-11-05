import json

def get_associated_nodes(node_id):

    scene_graph = json.load(open('../data/sceneGraphs/3dsg_withCOR.json', 'r'))

    # Build lookup dictionaries for quick access
    id_to_node = {
        'spaces': {node['id']: node for node in scene_graph.get('spaces', [])},
        'elements': {node['id']: node for node in scene_graph.get('elements', [])},
        'components': {node['id']: node for node in scene_graph.get('components', [])}
    }

    # Initialize result lists
    associated_spaces = []
    associated_nodes = []

    # Find the input node in 'elements' or 'components'
    node = id_to_node['elements'].get(node_id) or id_to_node['components'].get(node_id)
    if not node:
        return json.dumps({'error': f'Node ID {node_id} not found in elements or components.'})

    # Get room IDs associated with the node
    room_value = node.get('room', '')
    room_ids = [rid.strip() for rid in room_value.split(',') if rid.strip()]

    # Retrieve associated space nodes
    for rid in room_ids:
        space_node = id_to_node['spaces'].get(rid)
        if space_node:
            associated_spaces.append(space_node)

    # Collect all nodes that have the same room IDs
    for category in ['elements', 'components']:
        for n in scene_graph.get(category, []):
            n_room_value = n.get('room', '')
            n_room_ids = [rid.strip() for rid in n_room_value.split(',') if rid.strip()]
            if set(room_ids) & set(n_room_ids):
                associated_nodes.append(n)

    # Prepare the result
    result = {
        'defect_node': node,
        'associated_spaces': associated_spaces,
        'associated_elements': associated_nodes
    }

    return json.dumps(result, indent=4)