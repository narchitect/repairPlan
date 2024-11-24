from openai import OpenAI
from typing import List
from data.robots2 import robots_withConfig
from utils.loader import extract_json, get_room_id_by_node_id

client = OpenAI(
    api_key='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')

def get_navigationPath_o1(defect_id: int, scene_graph) -> tuple[List[int], str]:
    defect_room_id = get_room_id_by_node_id(defect_id)
    prompt = f"""
        You are an expert in navigation planning with graph data.

        Given the following information:
        1. Building information in 3D Scene Graph: {scene_graph} 
        2. Defect_room_id: {defect_room_id}
        3. Robot storage location: {robots_withConfig["robot_storage"]}

        Task:
        1. Plan possible and the most optimal path from robot's storage to the defect's location, which passes the least number of rooms and doors to the defect location.
            - Represent the path as a sequence of room_id and door_id in the format: [room_id, door_id, ... ].
            - if you can't find the path, return the reason for the failure.
        2. Final Output should be in JSON format:
        {{
            "navigation_path": [room_id, door_id, room_id, door_id] (id should be integer)
            "reason": only if you can't find the path.
        }}
        """

    response = client.beta.chat.completions.parse(
        model="o1-preview",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    output = response.choices[0].message.content
    print(output)
    path_json = extract_json(output)

    
    if not path_json["navigation_path"]:  
        return path_json["reason"]

    return path_json["navigation_path"]


