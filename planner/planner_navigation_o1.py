from openai import OpenAI
from typing import List
from data.robots2 import robots_withConfig
from utils.loader import extract_json, get_room_id_by_node_id

client = OpenAI(
    api_key='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')

def get_navigationPath_o1(room_id: int, scene_graph, gpt_model: str = "gpt-4o") -> tuple[List[int], str]:
    scene_graph_links = scene_graph["links"]
    prompt = f"""
        You are an expert in graph searching and path planning.

        Given the following information:
        1. Room connections in the builiding: {scene_graph_links} 
        2. Defect_room_id: {room_id}
        3. Robot storage location: {robots_withConfig["robot_storage"]}

        Task:
        1. Find the most optimal path from robot's storage to the defect's location, which passes the least number of rooms and doors to the defect location.
            - Represent the path as a sequence of room_id and door_id in the format: [room_id, door_id, ... ].
            - if you can't find the path, return the reason for the failure.
            - finding it by checking the graph,not providing the code to the user. 

        2. Provide your answer in JSON format:
        {{
            "navigation_path": [room_id, door_id, room_id, door_id] (id should be integer)
            "reason": only if you can't find the path.
        }}
        """

    response = client.chat.completions.create(
        model= gpt_model,
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


