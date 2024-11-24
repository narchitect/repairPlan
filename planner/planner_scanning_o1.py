from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Dict
from utils.loader import get_rooms_info, get_robot_info_by_id
import json

# Set your OpenAI API key
client = OpenAI(
    api_key='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')

# Function to find the optimal scanning location
def get_scanning_plan(defect_id, robot_id):
    selected_robot_info = get_robot_info_by_id(robot_id)
    camera_fov = selected_robot_info["robots"]["camera"]["FOV"]
    env_data = get_rooms_info(defect_id)

    prompt = f"""    
    Given the following information:
    Environment data: {env_data}
    Camera degrees Field of View (FOV): {camera_fov}

    Considering the given data, find the optimal camera location to scan the defect object and the optimal camera direction to scan the entire area of the defect.

    Please provide the reasoning steps as a chain of thought, include the formulas used, and finally output as:
    {{
        "optimal_location" : [x_coordinate, y_coordinate, z_coordinate],
        "optimal_direction": [ x_value, y_value, z_value ],
    }}
    """

    # Call the OpenAI API
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    output = response.choices[0].message.parsed

    return output.optimal_location, output.optimal_direction, output.reasoning