import json
import tiktoken
from utils.loader import GLOBAL_SCENE_GRAPH
def count_nodes_and_links(scene_graph_json, model_name="gpt-4o"):
    """
    씬 그래프 JSON 데이터를 분석하여 노드와 링크의 수를 세고,
    각 카테고리 및 전체 노드와 링크의 토큰 크기를 계산합니다.

    Args:
        scene_graph_json (dict): 씬 그래프를 나타내는 JSON 데이터.
        model_name (str): 사용할 OpenAI 모델 이름 (기본값: "gpt-3.5-turbo").

    Returns:
        dict: 노드 및 링크 수와 각 카테고리 및 전체의 토큰 크기를 포함한 결과.
    """
    # OpenAI의 모델에 맞는 인코더 선택
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # 모델 이름이 인코더에 등록되어 있지 않은 경우 기본 인코딩 사용
        encoding = tiktoken.get_encoding("cl100k_base")

    # 링크 수 계산
    links = scene_graph_json.get("links", [])
    total_links = len(links)

    # 노드 카테고리 초기화
    total_nodes = 0
    spaces_count = 0
    surfaces_count = 0
    components_count = 0

    # 토큰 크기 초기화
    spaces_token_size = 0
    surfaces_token_size = 0
    components_token_size = 0
    links_token_size = 0
    nodes_token_size = 0

    # 노드 카테고리 카운트
    if "nodes" in scene_graph_json:
        nodes = scene_graph_json["nodes"]
        spaces = nodes.get("spaces", [])
        surfaces = nodes.get("surfaces", [])
        components = nodes.get("components", [])

        spaces_count = len(spaces)
        surfaces_count = len(surfaces)
        components_count = len(components)

        # 총 노드 수 계산
        total_nodes = spaces_count + surfaces_count + components_count

        # 각 카테고리를 JSON 문자열로 변환 후 토큰 수 계산
        spaces_json = json.dumps(spaces, ensure_ascii=False)
        surfaces_json = json.dumps(surfaces, ensure_ascii=False)
        components_json = json.dumps(components, ensure_ascii=False)
        nodes_json = json.dumps(nodes, ensure_ascii=False)  # 전체 노드

        spaces_token_size = len(encoding.encode(spaces_json))
        surfaces_token_size = len(encoding.encode(surfaces_json))
        components_token_size = len(encoding.encode(components_json))
        nodes_token_size = len(encoding.encode(nodes_json))  # 전체 노드 토큰 수

    # 링크의 토큰 수 계산
    if links:
        links_json = json.dumps(links, ensure_ascii=False)
        links_token_size = len(encoding.encode(links_json))

    return {
        "total_nodes": total_nodes,
        "total_links": total_links,
        "spaces_count": spaces_count,
        "surfaces_count": surfaces_count,
        "components_count": components_count,
        "spaces_token_size": spaces_token_size,
        "surfaces_token_size": surfaces_token_size,
        "components_token_size": components_token_size,
        "nodes_token_size": nodes_token_size,       # 전체 노드 토큰 수
        "links_token_size": links_token_size        # 링크 토큰 수
    }



print(count_nodes_and_links(GLOBAL_SCENE_GRAPH))