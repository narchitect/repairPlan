import plotly.graph_objects as go
import numpy as np
from utils.loader import get_rooms_info


def visualize_scanning(defect_id, camera_fov, camera_location, camera_direction):
    env_data = get_rooms_info(defect_id)
    # 시야각(FOV) 정의
    fov = camera_fov

    # 타겟 위치 (결함 표면 위치)
    defect_loc = env_data['defect_node']['location']
    target_position = np.array([defect_loc['x'], defect_loc['y'], defect_loc['z']])

    # 카메라 위치와 방향 설정
    camera_position = np.array(camera_location)
    optimal_camera_direction = np.array(camera_direction)

    # 시각화를 위한 요소 필터링
    elements = env_data['associated_elements']
    fig = go.Figure()

    # 각 요소별로 시각화
    for elem in elements:
        elem_type = elem['type']
        elem_id = elem['id']
        loc = elem['location']
        size = elem['size']
        x_center, y_center, z_center = loc['x'], loc['y'], loc['z']
        dx, dy, dz = size['x'], size['y'], size['z']

        # 중심점에서 크기의 절반만큼 이동하여 코너 좌표 계산
        x0 = x_center - dx / 2
        x1 = x_center + dx / 2
        y0 = y_center - dy / 2
        y1 = y_center + dy / 2
        z0 = z_center - dz / 2
        z1 = z_center + dz / 2

        # Wall, Floor, Ceiling에 따라 면을 생성
        if elem_type == 'Wall' or elem_type in ['Floor', 'Ceiling']:
            thickness = 0.1
            if dx == 0.0:
                x0, x1 = x_center - thickness / 2, x_center + thickness / 2
            if dy == 0.0:
                y0, y1 = y_center - thickness / 2, y_center + thickness / 2
            if dz == 0.0:
                z0, z1 = z_center - thickness / 2, z_center + thickness / 2

            vertices = [[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
                        [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]]
            faces = [[0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
                     [0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5],
                     [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7]]
            x_vals, y_vals, z_vals = [v[0] for v in vertices], [v[1] for v in vertices], [v[2] for v in vertices]
            i, j, k = zip(*faces)

            color = 'red' if elem_id == env_data['defect_node']['id'] else (
                'lightblue' if elem_type == 'Wall' else 'lightgreen')

            fig.add_trace(go.Mesh3d(x=x_vals, y=y_vals, z=z_vals, i=i, j=j, k=k,
                                    color=color, opacity=0.5, flatshading=True, hoverinfo='skip'))

    # 카메라 위치 표시
    fig.add_trace(go.Scatter3d(x=[camera_position[0]], y=[camera_position[1]], z=[camera_position[2]],
                               mode='markers', marker=dict(size=5, color='black'), name='Camera Position'))

    # 타겟 위치 표시
    fig.add_trace(go.Scatter3d(x=[defect_loc['x']], y=[defect_loc['y']], z=[defect_loc['z']],
                               mode='markers', marker=dict(size=5, color='purple'), name='Target Position'))

    # 두 벡터 사이의 회전 행렬 계산 함수
    def rotation_matrix_from_vectors(vec1, vec2):
        a, b = (vec1 / np.linalg.norm(vec1)), (vec2 / np.linalg.norm(vec2))
        v = np.cross(a, b)
        c = np.dot(a, b)
        if c == -1:
            return -np.eye(3)
        elif c == 1:
            return np.eye(3)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + kmat + kmat @ kmat * ((1 - c) / (s ** 2))

    # FOV 원뿔 생성 함수
    def create_cone(apex, direction, angle, height, resolution=20):
        direction = direction / np.linalg.norm(direction)
        h, r = height, height * np.tan(np.radians(angle / 2))
        theta = np.linspace(0, 2 * np.pi, resolution)
        circle_x, circle_y, circle_z = np.ones_like(theta) * h, r * np.cos(theta), r * np.sin(theta)
        x, y, z = np.concatenate(([0], circle_x)), np.concatenate(([0], circle_y)), np.concatenate(([0], circle_z))

        cone_points = np.vstack((x, y, z)).T
        reference_direction = np.array([1, 0, 0])
        rotation_matrix = rotation_matrix_from_vectors(reference_direction, direction)
        rotated_points = cone_points @ rotation_matrix.T + apex
        return rotated_points[:, 0], rotated_points[:, 1], rotated_points[:, 2]

    # 원뿔 생성 및 추가
    cone_height = np.linalg.norm(target_position - camera_position)
    x_cone, y_cone, z_cone = create_cone(camera_position, optimal_camera_direction, fov, cone_height)

    i, j, k = [0] * (len(x_cone) - 2), list(range(1, len(x_cone) - 1)), list(range(2, len(x_cone)))
    i.append(0);
    j.append(len(x_cone) - 1);
    k.append(1)

    fig.add_trace(go.Mesh3d(x=x_cone, y=y_cone, z=z_cone, i=i, j=j, k=k,
                            opacity=0.2, color='yellow', name='Field of View'))

    # 그래프 설정
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', visible=True),
            yaxis=dict(title='Y', visible=True),
            zaxis=dict(title='Z', visible=True),
            aspectmode='data',
            aspectratio=dict(x=1, y=1, z=1),  
        ),
        title='Visualization on the optimal scanning position and direction',
        width=1200,
        height=800,
    )

    # 그래프 표시
    fig.show()

# # 함수 호출 예시
# gpt4o1_env  = {
#     'defect_node': {'id': '396', 'ifc_guid': '26kn7MqLL9oOOTivXpgDH8', 'type': 'Wall',
#                     'location': {'x': -0.26, 'y': -33.5286, 'z': 1.85},
#                     'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
#     'associated_spaces': [
#         {'id': '330', 'ifc_guid': '0x8tDwgKz4rBhuBSTQ03Vo', 'type': 'Space',
#          'location': {'x': -5.15925, 'y': -33.5286, 'z': 7.85},
#          'size': {'x': 9.799, 'y': 7.86, 'z': 3.7}}
#     ],
#     'associated_elements': [
#         {'id': '396', 'ifc_guid': '26kn7MqLL9oOOTivXpgDH8', 'type': 'Wall',
#          'location': {'x': -0.26, 'y': -33.5286, 'z': 1.85},
#          'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
#         {'id': '474', 'ifc_guid': '1T7BPQ_hn69uk5$Jp8cv99', 'type': 'Ceiling',
#          'location': {'x': -5.15925, 'y': -33.5286, 'z': 3.7},
#          'size': {'x': 9.799, 'y': 7.86, 'z': 0.0}, 'room': '330'},
#         {'id': '707', 'ifc_guid': '0a$DTcOc10$eWx3Py5JFns', 'type': 'Floor',
#          'location': {'x': -5.15925, 'y': -33.5286, 'z': 0.0},
#          'size': {'x': 9.799, 'y': 7.86, 'z': 0.0}, 'room': '330'},
#         {'id': '779', 'ifc_guid': '26kn7MqLL9oOOTivXpgCJg', 'type': 'Wall',
#          'location': {'x': -5.15925, 'y': -29.5986, 'z': 1.85},
#          'size': {'x': 9.799, 'y': 0.0, 'z': 3.7}, 'room': '330'},
#         {'id': '792', 'ifc_guid': '1XD1GHfzD6cunMzxtqLi4o', 'type': 'Wall',
#          'location': {'x': -10.0585, 'y': -33.5286, 'z': 1.85},
#          'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
#         {'id': '818', 'ifc_guid': '26kn7MqLL9oOOTivXpgDiH,26kn7MqLL9oOOTivXpgDiH', 'type': 'Wall',
#          'location': {'x': -5.15925, 'y': -37.4586, 'z': 1.85},
#          'size': {'x': 9.799, 'y': 0.0, 'z': 3.7}, 'room': '330'},
#     ]
# }


# gpt4o_answer = [-2.11, -33.5286, 1.85]
# gpt4o1_answer = [-4.605, -33.5286,  1.85]
# visualize_scanning(gpt4o1_env, camera_fov=90, camera_location=gpt4o1_answer, camera_direction=[1, 0, 0])
