import json

# JSON 파일 경로
json_file = "../data/graphs/BIM_Large/output.json"

# JSON 파일 로드 및 `node_type` 종류 추출
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# `node_type` 종류를 집합으로 수집하여 고유한 값만 저장
node_types = set(node["node_type"] for node in data["nodes"])

# 결과 출력
print("Node types:", node_types)
