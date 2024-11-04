import json
import openai
import re
from pydantic import BaseModel
from typing import List

json_schema = {
    "type": "object",
    "properties": {
        "defect_node": {
            "type": "string",
            "description": "The defect node id in 3D scene graphs based on user description."
        },
        "selected_robots": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The identifiers of the robots that are both reachable and accessible to the defect location."
            },
        "navigation_paths": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Sequence of identifiers representing the navigation path in the format: `[room1, door1, room2, door2, ..., roomN]`."
            },
        "reasoning": {
            "type": "string",
            "description": "Comprehensive step-by-step reasoning for all decisions made.",
        }
    },
    "required": ["defect_node", "selected_robots", "navigation_paths", "reasoning"],
    "additionalProperties": False
}



def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph


def generate_prompt(scene_graph, robots):
    prompt = f"""
        You are an expert in building repairs and navigation, with in-depth knowledge of various robot capabilities.

        3D Scene Graph:
        Here is a 3D scene graph representation of the environment:
        {scene_graph}

        Robots Available:
        {robots}

        Tasks:
        1. **Identify Defect**:**
           - Analyze the user's defect description 
           - identify the target defect node within the 3D scene graph.
           - **Reasoning:** Provide detailed reasoning for identifying this defect.

        2. **Check Reachability:**
           - Compare each robot's `max_reach_height` with the defect location's height.
           - **Reachable Robots:** List all robots that can reach the defect.
           - **Reasoning:** Explain why each robot is considered reachable or not.

        3. **Generate Navigation Paths:**
           - Create possible and optimal navigation path to the defect location.
           - Represent the path as a sequence of `room_id` and `door_id` in the format: `[room1, door1, room2, door2, ..., roomN]`.
           - Extract and list all doors present in each path.
           - **Reasoning:** Describe how you constructed each navigation path.


        4. **Check Accessibility:**
           - For the navigation path, compare the door sizes with each robot's size to determine accessibility.
           - **Reasoning:** Explain the accessibility assessment for each robot through the doors.
           - **Accessible Robots:** List robots that can access through the doors on the path.
           - If no robots can access a path, regenerate the navigation path until at least one robot can access.

        5. **Final Output:**
           - Provide a JSON object with the following structure:
             {{
               "defect_node": "defect_node_id",
               "defect_node_ifcGUID": "defect_node_ifcGUID",
               "selected_robots": ["robot_id", "robot_id", ...],
               "navigation_paths": [
                   {{
                       "path": ["room id", "door id", "room id", "door id", "room id"],
                   }},
               ],
               "reasoning": "Comprehensive step-by-step reasoning for all decisions made."
             }}

        **Constraints:**
        - Ensure that the selected robots have the necessary actions to address the defect.
        - Maintain clear and logical reasoning for each step.
        - Structure your response by first detailing your reasoning for each task, followed by the final JSON output.
        
        **Example Format:**
        1. **Identify Defect:**
           - Reasoning: [Your detailed reasoning here.]
        
        2. **Check Reachability:**
           - Reasoning: [Your detailed reasoning here.]
           """
    return prompt


def get_navigation_plan(user_input, scene_graph, robots):
    prompt_template = generate_prompt(scene_graph, robots)
    system_prompt = prompt_template
    user_message = user_input

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "navigation_plan",
                "strict": True,
                "schema": json_schema
            }
        },
        max_tokens=2500,
    )

    full_response = response.choices[0].message.content

    # Extract the JSON part from the response
    json_match = re.search(r'```json\n(.*?)\n```', full_response, re.DOTALL)
    if json_match:
        json_output = json_match.group(1)
        try:
            json_output = json.loads(json_output)  # JSON 문자열을 파이썬 객체로 변환
        except json.JSONDecodeError:
            print("JSON 디코딩 오류가 발생했습니다.")
    else:
        print("JSON 출력 부분을 찾을 수 없습니다.")

    return full_response, json_output