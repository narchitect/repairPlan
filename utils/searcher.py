import json

# 글로벌 변수로 고수준 및 전체 씬 그래프 데이터를 관리합니다.
high_level_scene_graph = {
    "spaces": [
        {
            "id": 1001,
            "elements": [2001, 2002]
        },
        {
            "id": 1002,
            "elements": [2003]
        }
    ]
}

full_scene_graph = {
    "spaces": [
        {
            "id": 1001,
            "elements": [2001, 2002]
        },
        {
            "id": 1002,
            "elements": [2003]
        }
    ],
    "elements": [
        {
            "id": 2001,
            "type": "wall",
            "components": [3001, 3002]
        },
        {
            "id": 2002,
            "type": "ceiling",
            "components": []
        },
        {
            "id": 2003,
            "type": "floor",
            "components": [3003]
        }
    ],
    "components": [
        {
            "id": 3001,
            "type": "window"
        },
        {
            "id": 3002,
            "type": "door"
        },
        {
            "id": 3003,
            "type": "vent"
        }
    ]
}

def find_node_by_id(node_id, node_type, data):
    """특정 유형 내에서 ID로 노드를 찾습니다."""
    for node in data.get(node_type, []):
        if node['id'] == node_id:
            return node
    return None

def expand_node(node_id):
    """글로벌 데이터를 사용하여 노드를 한 단계 확장합니다."""
    # 먼저 고수준 씬 그래프에서 노드를 찾습니다.
    node = find_node_by_id(node_id, 'spaces', high_level_scene_graph)
    if node:
        # 'elements'를 full_scene_graph에서 확장합니다.
        expanded_node = node.copy()
        expanded_elements = []
        for elem_id in node.get('elements', []):
            element = find_node_by_id(elem_id, 'elements', full_scene_graph)
            if element:
                # 'components'는 ID 목록으로 유지합니다.
                element_copy = element.copy()
                element_copy['components'] = element.get('components', [])
                expanded_elements.append(element_copy)
        expanded_node['elements'] = expanded_elements
        return expanded_node

    # spaces에서 찾지 못하면 elements에서 찾습니다.
    node = find_node_by_id(node_id, 'elements', full_scene_graph)
    if node:
        # 'components'를 full_scene_graph에서 확장합니다.
        expanded_node = node.copy()
        expanded_components = []
        for comp_id in node.get('components', []):
            component = find_node_by_id(comp_id, 'components', full_scene_graph)
            if component:
                # components는 더 이상 확장되지 않습니다.
                expanded_components.append(component.copy())
        expanded_node['components'] = expanded_components
        return expanded_node

    # node_id가 component인 경우
    node = find_node_by_id(node_id, 'components', full_scene_graph)
    if node:
        return node.copy()

    # 노드를 찾지 못한 경우
    return None

def contract_node(node_id):
    """노드를 ID와 자식 참조만 포함하도록 축소합니다."""
    # 고수준 씬 그래프에서 노드를 찾습니다.
    node = find_node_by_id(node_id, 'spaces', high_level_scene_graph)
    if node:
        contracted_node = {
            "id": node['id'],
            "elements": node.get('elements', [])
        }
        return contracted_node

    # elements에서 노드를 찾습니다.
    node = find_node_by_id(node_id, 'elements', full_scene_graph)
    if node:
        contracted_node = {
            "id": node['id'],
            "type": node.get('type', ''),
            "components": node.get('components', [])
        }
        return contracted_node

    # components에서 노드를 찾습니다.
    node = find_node_by_id(node_id, 'components', full_scene_graph)
    if node:
        contracted_node = {
            "id": node['id'],
            "type": node.get('type', '')
        }
        return contracted_node

    # 노드를 찾지 못한 경우
    return None

# 사용 예시:

print(high_level_scene_graph)

# ID가 1001인 공간을 확장합니다.
expanded_space = expand_node(1001)
print("Expanded Space (id 1001):")
print(json.dumps(expanded_space, indent=2))

# ID가 2001인 요소를 확장합니다.
expanded_element = expand_node(2001)
print("\nExpanded Element (id 2001):")
print(json.dumps(expanded_element, indent=2))

# ID가 1001인 공간을 축소합니다.
contracted_space = contract_node(1001)
print("\nContracted Space (id 1001):")
print(json.dumps(contracted_space, indent=2))

# ID가 2001인 요소를 축소합니다.
contracted_element = contract_node(2001)
print("\nContracted Element (id 2001):")
print(json.dumps(contracted_element, indent=2))
