import json

# JSON 파일 경로
json_file = "../data/graphs/BIM_COR/graphml_int.json"


# JSON 파일 읽기
with open(json_file, 'r') as file:
    data = json.load(file)

# node_type이 "element"인 노드에서 label 값 추출
labels = [node['label'] for node in data['nodes'] if node['node_type'] == 'element']

# 고유한 label 값 추출
unique_labels = set(labels)

print("Unique labels:", unique_labels)
