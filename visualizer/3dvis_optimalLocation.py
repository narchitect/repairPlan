data_str = """
{
    "defect_node": {
        "id": "537",
        "ifc_guid": "0a$DTcOc10$eWx3Py5JFns",
        "type": "Floor",
        "location": {"x": -26.1239, "y": -10.06045, "z": 0.0},
        "size": {"x": 8.168, "y": 5.181, "z": 0.0},
        "room": "119"
    },
    "associated_spaces": [
        {
            "id": "119",
            "ifc_guid": "0x8tDwgKz4rBhuBSTQ03Sx",
            "type": "Space",
            "location": {"x": -26.1239, "y": -10.06045, "z": 7.85},
            "size": {"x": 8.168, "y": 5.181, "z": 3.7}
        }
    ],
    "associated_elements": [
        {
            "id": "373",
            "ifc_guid": "08Kju84ofEuAMc6WrE1A36",
            "type": "Ceiling",
            "location": {"x": -26.1239, "y": -11.05785, "z": 3.0885},
            "size": {"x": 8.168, "y": 3.186319766191979, "z": 1.2230843583229625},
            "room": "119"
        },
        {
            "id": "537",
            "ifc_guid": "0a$DTcOc10$eWx3Py5JFns",
            "type": "Floor",
            "location": {"x": -26.1239, "y": -10.06045, "z": 0.0},
            "size": {"x": 8.168, "y": 5.181, "z": 0.0},
            "room": "119"
        },
        {
            "id": "573",
            "ifc_guid": "23aTbt_ibCF9nDuGzWAsXH",
            "type": "Wall",
            "location": {"x": -26.1239, "y": -7.47, "z": 1.85},
            "size": {"x": 8.168, "y": 0.0, "z": 3.7},
            "room": "119"
        },
        {
            "id": "590",
            "ifc_guid": "3P6tvjgV9AA81fRmsqfbUq",
            "type": "Wall",
            "location": {"x": -26.1239, "y": -12.6509, "z": 1.2385},
            "size": {"x": 8.168, "y": 0.0, "z": 2.477},
            "room": "119"
        },
        {
            "id": "659",
            "ifc_guid": "383DO$PSjCThEOrX4PKqGN",
            "type": "Wall",
            "location": {"x": -22.04, "y": -10.06045, "z": 1.85},
            "size": {"x": 0.0, "y": 5.181, "z": 3.7},
            "room": "119"
        },
        {
            "id": "762",
            "ifc_guid": "3P6tvjgV9AA81fRmsqfbRb",
            "type": "Wall",
            "location": {"x": -30.2078, "y": -10.06045, "z": 1.85},
            "size": {"x": 0.0, "y": 5.181, "z": 3.7},
            "room": "119"
        },
        {
            "id": "212",
            "ifc_guid": "383DO$PSjCThEOrX4PKqgQ",
            "type": "Door",
            "location": {"x": -21.97, "y": -8.120000000000001, "z": 1.013},
            "size": {"x": 0.19, "y": 1.252, "z": 2.026},
            "room": "119"
        }
    ]
}
"""

optimal_location_str = """
{
    "optimal_location": {
        "x": -26.1239,
        "y": -9.06045,
        "z": 1.5
    }
}
"""

import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import itertools

# 데이터 로드
data = json.loads(data_str)
optimal_location = json.loads(optimal_location_str)["optimal_location"]

# 3D 플롯 설정
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 축 레이블 설정
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 요소를 그리는 함수 정의

def draw_box_surface(ax, element, color='blue', alpha=0.5):
    x, y, z = element['location']['x'], element['location']['y'], element['location']['z']
    dx, dy, dz = element['size']['x'], element['size']['y'], element['size']['z']

    # 박스의 최소 및 최대 좌표 계산
    xmin = x - dx / 2
    xmax = x + dx / 2
    ymin = y - dy / 2
    ymax = y + dy / 2
    zmin = z - dz / 2
    zmax = z + dz / 2

    # 각 면을 그리기 위한 메쉬 생성
    # 상하면
    ax.plot_surface([[xmin, xmax], [xmin, xmax]], [[ymin, ymin], [ymax, ymax]], [[zmin, zmin], [zmin, zmin]], color=color, alpha=alpha)  # 아래면
    ax.plot_surface([[xmin, xmax], [xmin, xmax]], [[ymin, ymin], [ymax, ymax]], [[zmax, zmax], [zmax, zmax]], color=color, alpha=alpha)  # 윗면

    # 앞뒷면
    ax.plot_surface([[xmin, xmax], [xmin, xmax]], [[ymin, ymin], [ymin, ymin]], [[zmin, zmax], [zmin, zmax]], color=color, alpha=alpha)  # 앞면
    ax.plot_surface([[xmin, xmax], [xmin, xmax]], [[ymax, ymax], [ymax, ymax]], [[zmin, zmax], [zmin, zmax]], color=color, alpha=alpha)  # 뒷면

    # 좌우면
    ax.plot_surface([[xmin, xmin], [xmin, xmin]], [[ymin, ymax], [ymin, ymax]], [[zmin, zmax], [zmin, zmax]], color=color, alpha=alpha)  # 왼쪽면
    ax.plot_surface([[xmax, xmax], [xmax, xmax]], [[ymin, ymax], [ymin, ymax]], [[zmin, zmax], [zmin, zmax]], color=color, alpha=alpha)  # 오른쪽면
def draw_box(ax, element, color='blue', alpha=1.0, label=None):
    x, y, z = element['location']['x'], element['location']['y'], element['location']['z']
    dx, dy, dz = element['size']['x'], element['size']['y'], element['size']['z']

    # 박스의 최소 및 최대 좌표 계산
    xmin = x - dx / 2
    xmax = x + dx / 2
    ymin = y - dy / 2
    ymax = y + dy / 2
    zmin = z - dz / 2
    zmax = z + dz / 2

    # 박스의 모서리 좌표 리스트 생성
    xx = [xmin, xmax]
    yy = [ymin, ymax]
    zz = [zmin, zmax]

    # 모든 모서리에 대한 좌표 생성 및 그리기
    for s, e in itertools.product(itertools.combinations(xx, 2), itertools.combinations(yy, 2)):
        ax.plot3D([s[0], s[1]], [e[0], e[1]], [zmin, zmin], color=color, alpha=alpha)
        ax.plot3D([s[0], s[1]], [e[0], e[1]], [zmax, zmax], color=color, alpha=alpha)
    for s, e in itertools.product(itertools.combinations(xx, 2), itertools.combinations(zz, 2)):
        ax.plot3D([s[0], s[1]], [ymin, ymin], [e[0], e[1]], color=color, alpha=alpha)
        ax.plot3D([s[0], s[1]], [ymax, ymax], [e[0], e[1]], color=color, alpha=alpha)
    for s, e in itertools.product(itertools.combinations(yy, 2), itertools.combinations(zz, 2)):
        ax.plot3D([xmin, xmin], [s[0], s[1]], [e[0], e[1]], color=color, alpha=alpha)
        ax.plot3D([xmax, xmax], [s[0], s[1]], [e[0], e[1]], color=color, alpha=alpha)

    # 레이블 추가 (범례용)
    if label:
        ax.plot([], [], [], color=color, label=label)

# 환경 요소 그리기
for element in data['associated_elements']:
    draw_box(ax, element, color='blue', alpha=0.1)

# 결함 노드 그리기 (빨간색)
draw_box(ax, data['defect_node'], color='red', alpha=0.5, label='Defect Node')

# 최적 위치 표시 (녹색 점)
ax.scatter(optimal_location['x'], optimal_location['y'], optimal_location['z'], color='green', s=100, label='Optimal Location')

# 결함 노드 위치
defect_location = data['defect_node']['location']

# 카메라 방향을 결함 노드로 설정
direction = [
    defect_location['x'] - optimal_location['x'],
    defect_location['y'] - optimal_location['y'],
    defect_location['z'] - optimal_location['z']
]

# 방향 벡터를 정규화
direction = np.array(direction)
direction = direction / np.linalg.norm(direction)

# 시야각과 최대 거리 설정
fov = 60  # degrees
max_range = 3  # meters

# 시야각 시각화
def draw_fov_cone(ax, position, direction, fov, max_range, color='green', alpha=0.2):
    # 원뿔의 높이와 반지름 계산
    height = max_range
    radius = height * np.tan(np.radians(fov / 2))

    # 원뿔의 축을 Z축으로 맞추기 위한 회전 행렬 계산
    def rotation_matrix(a, b):
        a = a / np.linalg.norm(a)
        b = b / np.linalg.norm(b)
        v = np.cross(a, b)
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        I = np.eye(3)
        if s == 0:
            return I if c > 0 else -I
        kmat = np.array([[0, -v[2], v[1]],
                         [v[2], 0, -v[0]],
                         [-v[1], v[0], 0]])
        return I + kmat + kmat @ kmat * ((1 - c) / (s ** 2))

    # Z축 방향 벡터
    z_axis = np.array([0, 0, 1])
    R = rotation_matrix(z_axis, direction)

    # 원뿔 생성
    theta = np.linspace(0, 2 * np.pi, 30)
    h = np.linspace(0, height, 10)
    theta, h = np.meshgrid(theta, h)
    X = (h * radius / height) * np.cos(theta)
    Y = (h * radius / height) * np.sin(theta)
    Z = h

    # 원뿔 회전 및 이동
    XYZ = np.stack([X.flatten(), Y.flatten(), Z.flatten()], axis=1)
    XYZ = XYZ @ R.T
    X = XYZ[:, 0].reshape(theta.shape) + position['x']
    Y = XYZ[:, 1].reshape(theta.shape) + position['y']
    Z = XYZ[:, 2].reshape(theta.shape) + position['z']

    ax.plot_surface(X, Y, Z, color=color, alpha=alpha)

# 시야각 그리기
draw_fov_cone(ax, optimal_location, direction, fov, max_range, color='green', alpha=0.2)

# 결함 노드가 시야각 내에 있는지 확인하는 함수
def is_in_fov(optimal_location, target_location, direction, fov, max_range):
    # 최적 위치에서 결함 노드까지의 벡터 계산
    vec = np.array([
        target_location['x'] - optimal_location['x'],
        target_location['y'] - optimal_location['y'],
        target_location['z'] - optimal_location['z']
    ])
    distance = np.linalg.norm(vec)
    if distance > max_range:
        return False

    # 방향 벡터와의 각도 계산
    cos_angle = np.dot(vec, direction) / (np.linalg.norm(vec) * np.linalg.norm(direction))
    angle = np.degrees(np.arccos(cos_angle))

    return angle <= (fov / 2)

# 결함 노드가 시야각 내에 있는지 확인
if is_in_fov(optimal_location, defect_location, direction, fov, max_range):
    print("결함 노드가 시야각 내에 있습니다.")
else:
    print("결함 노드가 시야각 내에 없습니다.")

# 플롯 범위 설정
ax.set_xlim(-32, -20)
ax.set_ylim(-15, -5)
ax.set_zlim(0, 4)

# 범례 표시
ax.legend()

# 그래프 표시
plt.show()


