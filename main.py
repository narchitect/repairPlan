import json
import openai
from pydantic import BaseModel
from typing import List


class NavigationPlan(BaseModel):
    defect_object: str
    room_seqeunce: List[str]
    actions: List[str]


def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph


def generate_prompt(scene_graph):
    prompt = f"""
    You are an expert in building repairs. Here is a 3D scene graph representation of the environment: {scene_graph}.
    Your task is to:
    1. Identify the defect node based on the user's description from 3D scene graphs
    2. Generate a navigation path to the defect location in room scale
    3. Provide the sequence of actions to move to the defect location
    
    The output format should strictly adhere to the following JSON structure:
    {{
      "defect_object": "object_name_from_3D_scene",
      "room_sequence": ["room1", "room2", "room3"],
      "actions": ["moveto(room1)", "open(door1)", "moveto(room4)"]
    }}
    """

    return prompt


def get_navigation_plan(user_input, scene_graph_path):
    scene_graph = load_scene_graph(scene_graph_path)
    prompt = generate_prompt(scene_graph)

    response = openai.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.choices[0].message


def main():
    scene_graph_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/scene_graph_final.json"
    user_input = "the window in the meeting room is broken and I'm currently in office_1"
    result = get_navigation_plan(user_input, scene_graph_path)
    print(result.content)


if __name__ == "__main__":
    main()
