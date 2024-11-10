import json

def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph