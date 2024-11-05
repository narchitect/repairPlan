import json
from openai import OpenAI

client = OpenAI(api_key='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')

def plan_robot_task(user_info, robot_info, env_info):

    prompt = f"""
    You are an expert in robot task planning for building maintenance.

    Given the following information:

    User Defect Description:
    {user_info}

    Robot Library:
    {json.dumps(robot_info, indent=2)}

    Environment Information:
    {json.dumps(env_info, indent=2)}

    Important:
    - The robot's actions are defined with parameters, e.g., 'navigateTo<object>'.
    - Use appropriate parameters enclosed in '<>', where '<object>' is the node ID from the 3D scene graph.
    - Ensure that the action sequence uses node IDs from the environment data.
    - Consider the relationship between actions and the equipment loaded.
    - The robot is a one-arm robot; it can only load one equipment at a time.
    - The robot must unload equipment before loading another equipment.
    - At the end of the task, the robot should unload all equipment.

    Your tasks are:
    1. Select the most efficient robot from the robot library to repair the defect described.
    2. Generate a detailed action sequence for the selected robot to perform the repair, based on its capabilities and the provided environment information.
    3. Include parameters in the actions as defined in the robot's action list, using node IDs from the 3D scene graph.

    Please output your answer in JSON format as:
    {{
        "selected_robot_id": "<robot_id>",
        "action_sequence": [
            "<First action>",
            "<Second action>",
            ...
        ]
    }}
    """

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": "You are an assistant that helps with robot action planning."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2500,
        temperature=0,
    )

    full_response = response.choices[0].message.content
    return full_response

