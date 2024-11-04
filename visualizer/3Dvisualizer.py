
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# 데이터 로드
data = main.load_scene_graph("data/scene_graph_final.json")

# 그래프 생성
G = nx.Graph()

# 노드 및 엣지 추가 (이전과 동일)

# 3D 위치 계산
pos = nx.spring_layout(G, dim=3, k=0.15, iterations=50)
node_xyz = np.array([pos[v] for v in G.nodes()])

# 노드 타입별 색상 및 크기 설정
node_types = nx.get_node_attributes(G, 'type')
type_to_color = {'room': 'blue', 'object': 'green', 'asset': 'red', 'unknown': 'gray'}
node_colors = [type_to_color.get(node_types.get(node, 'unknown'), 'gray') for node in G.nodes()]

# 노드와 엣지의 정보를 Plotly 데이터로 변환
edge_xyz = []
for edge in G.edges():
    edge_xyz.append((pos[edge[0]], pos[edge[1]]))

# 3D 위치 계산
pos = nx.spring_layout(G, dim=3, k=0.15, iterations=50)

print(pos)

node_xyz = np.array([pos[v] for v in G.nodes()])
edge_xyz = [(pos[u], pos[v]) for u, v in G.edges()]

# 3D 그래프 생성
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# 노드 그리기
ax.scatter(node_xyz[:, 0], node_xyz[:, 1], node_xyz[:, 2], s=20, c='b', depthshade=True)

# 엣지 그리기
for edge in edge_xyz:
    x_coords = [edge[0][0], edge[1][0]]
    y_coords = [edge[0][1], edge[1][1]]
    z_coords = [edge[0][2], edge[1][2]]
    ax.plot(x_coords, y_coords, z_coords, c='gray')

plt.show()

