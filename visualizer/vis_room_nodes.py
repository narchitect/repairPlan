import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg

def visualize_room_nodes(room_node_id):
    # 장면 그래프 로드
    from utils.loader import load_scene_graph
    scene_graph_full = load_scene_graph("/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/new_structure/3dsg_full.json")
    
    # 이미지 경로 설정
    image_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/images/top_view.png"
    output_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/images/room0_nodes.png"
    
    # 배경 이미지 로드
    img = mpimg.imread(image_path)
    
    # 그래프 생성
    G = nx.Graph()
    
    # 참조점과 스케일 팩터 설정 (필요에 따라 조정)
    reference_point_img = (333, 10)
    scale_factor = 9.8

    # Room 노드를 찾아서 해당 서페이스 및 컴포넌트 시각화
    selected_room = next((room for room in scene_graph_full['nodes']['spaces'] if room['id'] == room_node_id), None)
    
    if not selected_room:
        print(f"Room with ID {room_node_id} not found.")
        return

    # Room 노드 추가
    x, y, z = selected_room['location']
    adjusted_x = (x * scale_factor) + reference_point_img[0]
    adjusted_y = reference_point_img[1] - (y * scale_factor)

    # Room 노드 설정 (기본 위치)
    room_node_id_str = f"{selected_room['id']}"
    G.add_node(
        room_node_id_str,
        pos=(adjusted_x, adjusted_y),
        node_type='space'
    )

    # 해당 Room에 연결된 Surfaces 추가
    for surface_id in selected_room['surfaces']:
        surface = next((s for s in scene_graph_full['nodes']['surfaces'] if s['id'] == surface_id), None)
        if not surface:
            continue
        
        # Surface 위치 설정
        x, y, z = surface['location']
        adjusted_x_surface = (x * scale_factor) + reference_point_img[0]
        adjusted_y_surface = reference_point_img[1] - (y * scale_factor)

        # Surface 타입에 따른 위치 조정
        surface_type = surface.get('type', 'unknown')
        if surface_type == 'floor':
            adjusted_x_surface -= 5  # floor는 room 노드 왼쪽에 배치
        elif surface_type == 'ceiling':
            adjusted_x_surface += 5 # ceiling은 room 노드 오른쪽에 배치

        surface_node_id_str = f"{surface['id']}"
        G.add_node(
            surface_node_id_str,
            pos=(adjusted_x_surface, adjusted_y_surface),
            node_type=surface_type
        )
        
        # Surface와 Room 간 엣지 추가
        G.add_edge(room_node_id_str, surface_node_id_str)

        # 해당 Surface에 연결된 Components 추가
        for component_id in surface.get('components', []):
            component = next((c for c in scene_graph_full['nodes']['components'] if c['id'] == component_id), None)
            if not component:
                continue
            
            # Component 위치 설정
            x, y, z = component['location']
            adjusted_x_component = (x * scale_factor) + reference_point_img[0]
            adjusted_y_component = reference_point_img[1] - (y * scale_factor)

            # Component 위치 조정 (다른 Surface와 겹치지 않게 추가 이동)
            adjusted_x_component += 10  # Component는 약간 오른쪽으로 이동하여 겹침 방지

            component_node_id_str = f"{component['id']}"
            G.add_node(
                component_node_id_str,
                pos=(adjusted_x_component, adjusted_y_component),
                node_type=component.get('type', 'unknown')
            )
            
            # Component와 Surface 간 엣지 추가
            G.add_edge(surface_node_id_str, component_node_id_str)

    
    # 노드 위치와 타입 추출
    pos = nx.get_node_attributes(G, 'pos')
    node_types = nx.get_node_attributes(G, 'node_type')
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img)
    ax.set_xlim(0, img.shape[1])
    ax.set_ylim(img.shape[0], 0)
    ax.axis("equal")
    ax.axis('off')
    
    # 노드 색상 지정
    node_colors = []
    for node in G.nodes:
        n_type = node_types[node]
        if n_type == 'space':
            node_colors.append('blue')
        elif n_type == 'wall':
            node_colors.append('green')
        elif n_type == 'floor':
            node_colors.append('brown')
        elif n_type == 'ceiling':
            node_colors.append('purple')
        elif n_type == 'door':
            node_colors.append('red')
        elif n_type == 'window':
            node_colors.append('orange')
        else:
            node_colors.append('gray')
    
    # 그래프 그리기
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        edge_color='gray',
        node_size=500,
        font_size=10,
        font_color='white',
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, transparent=False)
    plt.show()


# Room 노드 ID를 지정하여 호출
visualize_room_nodes(room_node_id=0)
