from openai import OpenAI
from utils.loader import get_rooms_info, get_robot_info_by_id, extract_json


# Set your OpenAI API key
client = OpenAI(
    api_key='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')

# Function to find the optimal scanning location
def get_scanning_plan_o1(defect_id, robot_id, gpt_model: str = "gpt-4o"):
    selected_robot_info = get_robot_info_by_id(robot_id)
    camera_fov = selected_robot_info["robots"]["camera"]["FOV"]
    env_data = get_rooms_info(defect_id)

    prompt = f"""
    You are an expert in scanning camera positioning.

    Given the following information:
    Environment data: {env_data}
    Camera degrees Field of View (FOV): {camera_fov}

    Task:
    - Find the optimal camera location within the defect's room to scan the defect object and the optimal camera direction to scan the entire area of the defect.
    - every windows are linked to the indoor walls.
    - if you can't find them, return the reason.
    
    Final Output should be in JSON format:
    {{
        "optimal_location" : [x_coordinate, y_coordinate, z_coordinate],
        "optimal_direction": [x_value, y_value, z_value],
        "reason": only if you can't find the optimal location and direction.
    }}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model= gpt_model,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    output = response.choices[0].message.content
    print(output)
    output_json = extract_json(output)

    return output_json["optimal_location"], output_json["optimal_direction"]
