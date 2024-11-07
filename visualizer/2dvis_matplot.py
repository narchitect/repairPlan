import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.image as mpimg
from planner.planner import load_scene_graph

# 데이터 로드
data = load_scene_graph("../data/sceneGraphs/3dsg_withCOR.json")

# 배경 이미지 로드
img = mpimg.imread('../data/image/top_view.png')  # 렌더링된 이미지 파일 경로 입력

# 네트워크 그래프 생성
G = nx.Graph()

# Reference Point 및 스케일 설정
reference_point_img = (333, 10)  # 이미지에서의 reference point 좌표
reference_point_graph = (0, 0)     # 그래프에서의 reference point 좌표
scale_factor = 9.8  # 이미지와 그래프의 스케일을 맞추기 위한 비율 (필요시 조정)

# 공간 노드 추가 및 위치 조정
for space in data['spaces']:
    x, y = space['location']['x'], space['location']['y']
    # 오프셋 및 스케일 조정
    adjusted_x = (x * scale_factor) + reference_point_img[0]
    adjusted_y = reference_point_img[1] - (y * scale_factor)  # y 값을 반전
    G.add_node(space['id'], pos=(adjusted_x, adjusted_y), node_type='Space')  # 조정된 위치로 노드 추가

# 문과 창문을 그래프에 추가
for component in data['components']:
    if component['type'] in ['Door', 'Window']:
        x, y = component['location']['x'], component['locati']['y']
        adjusted_x = (x * scale_factor) + reference_point_img[0]
        adjusted_y = reference_point_img[1] - (y * scale_factor)
        G.add_node(component['id'], pos=(adjusted_x, adjusted_y), node_type=component['type'])
# 노드 위치 추출
pos = nx.get_node_attributes(G, 'pos')
node_types = nx.get_node_attributes(G, 'node_type')


#배경 이미지 위에 그래프 오버레이 설정
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(img)

# 축 범위를 이미지와 동일하게 설정 (필요시 조정)
ax.set_xlim(0, 420)    # 이미지 너비
ax.set_ylim(1256, 0)

ax.axis("equal")

# 노드 색상 설정
node_colors = [
    'blue' if node_types[node] == 'Space' else
    'green' if node_types[node] == 'Door' else
    'red' for node in G.nodes
]

# 그래프를 이미지 위에 오버레이
nx.draw(
    G,
    pos,
    ax=ax,
    with_labels=True,
    node_color=node_colors,
    edge_color='gray',
    node_size=300,
    font_size=8,
    font_color='black'
)

# 백그라운드 설정
plt.tight_layout()

plt.savefig("graph_overlay.png", dpi=300, transparent=False)

# 그래프 출력

plt.show()

