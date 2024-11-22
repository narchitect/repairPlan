import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg
from utils.loader import load_scene_graph

def visualize_navigation(path, defect_id, data, image_path, output_path):       
    # 배경 이미지 로드
    img = mpimg.imread(image_path)  # 렌더링된 이미지 파일 경로 입력

    # 네트워크 그래프 생성
    G = nx.Graph()

    # Reference Point 및 스케일 설정
    reference_point_img = (333, 10)  # 이미지에서의 reference point 좌표
    reference_point_graph = (0, 0)     # 그래프에서의 reference point 좌표
    scale_factor = 9.8  # 이미지와 그래프의 스케일을 맞추기 위한 비율 (필요시 조정)

    # 공간 노드 추가 및 위치 조정
    for space in data['nodes']['spaces']:
        x, y, z= space['location']
        # 오프셋 및 스케일 조정
        adjusted_x = (x * scale_factor) + reference_point_img[0]
        adjusted_y = reference_point_img[1] - (y * scale_factor)  # y 값을 반전
        G.add_node(space['id'], pos=(adjusted_x, adjusted_y), node_type='space')  # 조정된 위치로 노드 추가

    # 문과 창문을 그래프에 추가
    for component in data['nodes']['components']:
        if component['type'] in ['door', 'window']:
            x, y, z= component['location']
            adjusted_x = (x * scale_factor) + reference_point_img[0]
            adjusted_y = reference_point_img[1] - (y * scale_factor)
            G.add_node(component['id'], pos=(adjusted_x, adjusted_y), node_type=component['type'])
    
    
    # 경로에 포함된 노드와 엣지를 순서대로 추가
    H = nx.DiGraph()  # 방향 그래프로 생성하여 화살표 순서를 명확히 함

    # 순서대로 노드와 엣지 추가
    for i in range(len(path)):
        node_id = path[i]
        if node_id in G.nodes:
            # 노드를 H에 추가, G에서 위치와 타입 정보를 가져옴
            H.add_node(node_id, pos=G.nodes[node_id]['pos'], node_type=G.nodes[node_id]['node_type'])
        if i < len(path) - 1:
            # 순서에 맞게 엣지 추가
            H.add_edge(path[i], path[i + 1])

    # 결함 노드 추가 및 위치 조정
    for category in ['spaces', 'surfaces', 'components']:
        for defect in data['nodes'][category]:
            if defect['id'] == defect_id:
                x, y, z = defect['location']
                adjusted_x = (x * scale_factor) + reference_point_img[0]
                adjusted_y = reference_point_img[1] - (y * scale_factor)
                G.add_node(defect['id'], pos=(adjusted_x, adjusted_y), node_type='defect')
                H.add_node(defect['id'], pos=(adjusted_x, adjusted_y), node_type='defect')

    # 노드 위치와 타입 추출
    pos = nx.get_node_attributes(H, 'pos')
    node_types = nx.get_node_attributes(H, 'node_type')

    # 배경 이미지 위에 그래프 오버레이 설정
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img)

    # 축 범위를 이미지와 동일하게 설정 (필요시 조정)
    ax.set_xlim(0, 420)    # 이미지 너비
    ax.set_ylim(1256, 0)
    ax.axis("equal")

    # 노드 색상 설정
    node_colors = [
        'blue' if node_types[node] == 'space' else
        'green' if node_types[node] == 'door' else
        'red' if node_types[node] == 'window' else
        'orange' if node_types[node] == 'defect' else 'gray' for node in H.nodes  # 결함 노드는 주황색으로 설정
    ]

    # 경로에 포함된 그래프를 이미지 위에 오버레이
    nx.draw(
        H,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        edge_color='gray',
        node_size=300,
        font_size=8,
        font_color='black',
        arrows=True,
        arrowsize=20,
        arrowstyle='->',
    )

    # 백그라운드 설정 및 저장
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, transparent=False)
    plt.show()

# 함수 사용 예시
# overlay_navigation_path(["332","14", "330", "22", "328", "320"], load_scene_graph("../data/sceneGraphs/3dsg_withCOR.json"), '../data/image/top_view.png', "navigation_path_overlay2.png")
