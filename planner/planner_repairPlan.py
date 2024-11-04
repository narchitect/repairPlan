import json
from openai import OpenAI

client = OpenAI(api_key='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')

def plan_robot_task(defect_info, user_description, robots):
    selected_robot_ids = defect_info['selected_robots']
    selected_robots = [robot for robot in robots if robot['id'] in selected_robot_ids]

    prompt = f"""
    You are an expert in robot task planning.
    Given the following defect information:
        - Defect Node: {defect_info['defect_node']}
        - Defect Node IFC GUID: {defect_info['defect_node_ifcGUID']}
        - Selected Robots: {[robot['id'] for robot in selected_robots]}
        - Reasoning: {defect_info['reasoning']}
        
        User Description on Defects:
        "{user_description}"
        
        Robot Definitions:
        {json.dumps(selected_robots)}
        
        From the above information:
        1. Select the best robot to perform the repair, considering the robot's actions and the defect case.
        2. Suggest the specific tools necessary for the repair, which robot can hold.
        3. Propose an action sequence using the robot's possible actions to perform the repair.
        
        Output the result in JSON format as:
        {{
            "best_robot": "robot_id",
            "tools": ["tool1", "tool2", ...],
            "action_sequence": ["action1", "action2", ...]
        }}
    """

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for robot task planning."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2500,
        temperature=0,
    )

    full_response = response.choices[0].message.content
    return full_response

