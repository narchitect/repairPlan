import json
from openai import OpenAI
from utils.loader import get_room_infos, get_robot_info_by_id, extract_json

#initialize OpenAI client
client = OpenAI(api_key='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')

def get_repair_plan(user_info, defect_id, robot_id, gpt_model: str="gpt-4o"):
    room_info = get_room_infos(defect_id)
    robot_info = get_robot_info_by_id(robot_id)

    prompt = f"""
        You are a highly skilled expert in robotic task planning specifically for building maintenance.

        Please consider the following detailed information:

        User Defect Description:
        {user_info}

        Robot information:
        {json.dumps(robot_info, indent=2)}

        Environmental Context:
        {json.dumps(room_info, indent=2)}

        Key Considerations:
        - The robot is equipped with a single arm and can "load" only one piece of equipment at a time. It must "unload" before loading another.
        - Actions for the robot are parameterized, such as 'spray(element_id)', where 'element_id' is the node ID from the 3D scene graph.
        - Ensure that the action sequence strictly uses node IDs from the provided environmental data.
        - Carefully consider the relationship between each action and the equipment loaded.
        - At the conclusion of the task, ensure the robot unloads all equipment.

        Your objectives are:
        1. Develop a comprehensive and precise action sequence for the selected robot to execute the repair, leveraging its capabilities and the environmental context provided.
        2. Integrate parameters into the actions as specified in the robot's action list, utilizing node IDs from the 3D scene graph.

        The final output should be a JSON object with the following fields:
        - action_sequence: List[str]


        example output:
        {{
            "action_sequence": ['loadArm(sprayGun, cleaning Solution)', 'spray(4068)', 'unloadArm()', 'loadArm(wiper)', 'wipeSurface(4068)', 'unloadArm()'],
        }}
        """

    # API call
    response = client.chat.completions.create(
        model=gpt_model,  # Use a model that supports structured outputs
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content
    # print(output)
    output = extract_json(output)

    # Return the result
    return output['action_sequence']

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
