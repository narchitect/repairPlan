import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg

def visualize_all_nodes():
    # 장면 그래프 로드
    from utils.loader import load_scene_graph
    scene_graph_full = load_scene_graph("/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/new_structure/3dsg_full.json")
    
    # 이미지 경로 설정
    image_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/images/top_view.png"
    output_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/images/all_nodes_with_floor_ceiling.png"
    
    # 배경 이미지 로드
    img = mpimg.imread(image_path)
    
    # 그래프 생성
    G = nx.Graph()
    
    # 참조점과 스케일 팩터 설정 (필요에 따라 조정)
    reference_point_img = (333, 10)
    scale_factor = 9.8
    
    # 노드 추가
    for category in ['spaces', 'components', 'surfaces']:
        for node in scene_graph_full['nodes'].get(category, []):
            x, y, z = node['location']
            adjusted_x = (x * scale_factor) + reference_point_img[0]
            adjusted_y = reference_point_img[1] - (y * scale_factor)
            
            # 노드 타입 설정
            if category == 'spaces':
                node_type = 'space'
            else:
                node_type = node.get('type', 'unknown')

            # 노드 타입에 따라 좌표 조정
            if node_type == 'floor':
                adjusted_x -= 15  # floor는 room 노드 왼쪽에 배치
            elif node_type == 'ceiling':
                adjusted_x += 15  # ceiling은 room 노드 오른쪽에 배치

            # 노드 ID에 카테고리 접두사 추가
            node_id = f"{node['id']}"

            G.add_node(
                node_id,
                pos=(adjusted_x, adjusted_y),
                node_type=node_type
            )

    
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
            node_colors.append('yellow')
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
        node_size=100,
        font_size=6,
        font_color='black',
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, transparent=False)
    plt.show()



# Call the function
visualize_all_nodes()
