import json
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from data.robots import robots
from utils.loader import get_room_infos, get_robot_info_by_id

#initialize OpenAI client
client = OpenAI(api_key='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')

# Output schema
class RepairPlan(BaseModel):
    action_sequence: List[str]
    reasoning: str

def get_repair_plan(user_info, defect_id, robot_id, gpt_model: str="gpt-4o"):
    room_info = get_room_infos(defect_id)
    robot_info = get_robot_info_by_id(robot_id)

    prompt = f"""
        You are a highly skilled expert in robotic task planning specifically for building maintenance.

        Please consider the following detailed information:

        User Defect Description:
        {user_info}

        Robot Specifications:
        {json.dumps(robot_info, indent=2)}

        Environmental Context:
        {json.dumps(room_info, indent=2)}

        Task:
        1. suggest a sequence of actions to repair the defect based on the selected robot's capability and the environmental context
        2. ensure the parameters of the actions are correctly set
        3. once the robot has finished the task, it should unload all the equipment
        
        The final output should be a JSON object with the following fields:
        - action_sequence: List[str]
        - reasoning: str

        For example output:
        {
            "action_sequence": ["loadArm(sprayGun, cleaning Solution)", "spray(4068)", "unloadArm()", "loadArm(wiper)", "wipeSurface(4068)", "unloadArm()"],
        }
        """

    # API call
    response = client.beta.chat.completions.parse(
        model=gpt_model,  # Use a model that supports structured outputs
        messages=[
            {"role": "system", "content": "You are an assistant that helps with robot action planning."},
            {"role": "user", "content": prompt}
        ],
        response_format=RepairPlan,  # Use Pydantic model to define output schema
        temperature=0,
        max_tokens= 500,
    )

    output = response.choices[0].message.parsed
    # Return the result
    return output.action_sequence, output.reasoning

# Example function call
# user_info = "there is a stain on the wall"
# robot_info = robots
# data = {
#     'defect_node': {'id': '396', 'ifc_guid': '26kn7MqLL9oOOTivXpgDH8', 'type': 'Wall',
#                     'location': {'x': -0.26, 'y': -33.5286, 'z': 1.85},
#                     'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
#     'associated_spaces': [
#         {'id': '330', 'ifc_guid': '0x8tDwgKz4rBhuBSTQ03Vo', 'type': 'Space',
#          'location': {'x': -5.15925, 'y': -33.5286, 'z': 7.85},
#          'size': {'x': 9.799, 'y': 7.86, 'z': 3.7}}
#     ],
#     'associated_elements': [
#         {'id': '396', 'ifc_guid': '26kn7MqLL9oOOTivXpgDH8', 'type': 'Wall',
#          'location': {'x': -0.26, 'y': -33.5286, 'z': 1.85},
#          'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
#         {'id': '474', 'ifc_guid': '1T7BPQ_hn69uk5$Jp8cv99', 'type': 'Ceiling',
#          'location': {'x': -5.15925, 'y': -33.5286, 'z': 3.7},
#          'size': {'x': 9.799, 'y': 7.86, 'z': 0.0}, 'room': '330'},
#         {'id': '707', 'ifc_guid': '0a$DTcOc10$eWx3Py5JFns', 'type': 'Floor',
#          'location': {'x': -5.15925, 'y': -33.5286, 'z': 0.0},
#          'size': {'x': 9.799, 'y': 7.86, 'z': 0.0}, 'room': '330'},
#         {'id': '779', 'ifc_guid': '26kn7MqLL9oOOTivXpgCJg', 'type': 'Wall',
#          'location': {'x': -5.15925, 'y': -29.5986, 'z': 1.85},
#          'size': {'x': 9.799, 'y': 0.0, 'z': 3.7}, 'room': '330'},
#         {'id': '792', 'ifc_guid': '1XD1GHfzD6cunMzxtqLi4o', 'type': 'Wall',
#          'location': {'x': -10.0585, 'y': -33.5286, 'z': 1.85},
#          'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
#         {'id': '818', 'ifc_guid': '26kn7MqLL9oOOTivXpgDiH,26kn7MqLL9oOOTivXpgDiH', 'type': 'Wall',
#          'location': {'x': -5.15925, 'y': -37.4586, 'z': 1.85},
#          'size': {'x': 9.799, 'y': 0.0, 'z': 3.7}, 'room': '330'},
#     ]
# }
#
#
# result = plan_robot_task(user_info, robot_info, data)
# # print(result)
#
# print(result.selected_robot_id)
