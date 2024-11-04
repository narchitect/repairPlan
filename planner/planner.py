import json
import openai


def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph
def generate_prompt(scene_graph):
    prompt = f"""
    You are an expert in building repairs and navigation. 
    Here is a 3D scene graph representation of the environment: {scene_graph}.

    Your tasks are:
    1. Identify the defect node based on the user's description from the 3D scene graph.
    2. Generate a navigation path to the defect location at room scale.
    3. Provide the sequence of actions to move to the defect location 
        using the pre-defined functions: moveto(room_node), open(door_node), close(door_node).

    Provide a detailed step-by-step reasoning for your decisions.

    Remember, the output should be a JSON object matching the following structure:
    {{
      "defect_object": "object_name_from_3D_scene",
      "room_path": ["room1", "room2", "room3"],
      "actions": ["moveto('room1')", "open('door1')", "moveto('room3')"],
      "reasoning": "Your step-by-step reasoning here."
    }}
    """
    return prompt

def get_navigation_plan(user_input, prompt):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "moveto",
                "description": "Move the robot to a specified room node.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_node": {
                            "type": "string",
                            "description": "The name of the room node to move to."
                        }
                    },
                    "required": ["room_node"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "open_door",
                "description": "Open a specified door node.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "door_node": {
                            "type": "string",
                            "description": "The name of the door node to open."
                        }
                    },
                    "required": ["door_node"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "close_door",
                "description": "Close a specified door node.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "door_node": {
                            "type": "string",
                            "description": "The name of the door node to close."
                        }
                    },
                    "required": ["door_node"],
                    "additionalProperties": False
                }
            }
        }
    ]
    response = openai.chat.completions.create(
        tools=tools,
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
    return response


