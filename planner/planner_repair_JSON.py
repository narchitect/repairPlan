import json
import re
from openai import OpenAI
from jsonschema import validate, ValidationError
from data.robots import robots

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key='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')

# JSON Schema 정의
output_schema = {
    "type": "object",
    "properties": {
        "selected_robot_id": {"type": "string"},
        "action_sequence": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["selected_robot_id", "action_sequence"]
}


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
    - the robot is a one-arm robot, it must "load" only one equipment at once before doing a task and must "unload" before loading another one. 
    - The robot's actions are defined with parameters, e.g., 'navigateTo<object>'.
    - Use appropriate parameters enclosed in '<>', where '<object>' is the node ID from the 3D scene graph.
    - Ensure that the action sequence uses node IDs from the environment data.
    - Consider the relationship between actions and the equipment loaded.
    - At the end of the task, the robot should unload all equipment.

    Your tasks are:
    1. Select the most efficient and detailed robot from the robot library to repair the defect described.
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

    # API 호출
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are an assistant that helps with robot action planning."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0,
    )

    # 응답에서 JSON 부분 추출
    full_response = response.choices[0].message.content
    json_match = re.search(r'```json\n(.*?)\n```', full_response, re.DOTALL)

    if json_match:
        json_output = json_match.group(1)
        try:
            parsed_output = json.loads(json_output)

            # JSON Schema로 검증
            validate(instance=parsed_output, schema=output_schema)
            print("JSON 출력이 스키마를 준수합니다.")
            return parsed_output

        except (json.JSONDecodeError, ValidationError) as e:
            print("JSON 디코딩 오류 또는 스키마 검증 오류가 발생했습니다:", e)
    else:
        print("JSON 출력 부분을 찾을 수 없습니다.")
    return None


# 함수 호출 예시
user_info = "there is a stain on the ceiling in room id 320."
robot_info = robots
data = {
    'defect_node': {'id': '396', 'ifc_guid': '26kn7MqLL9oOOTivXpgDH8', 'type': 'Wall',
                    'location': {'x': -0.26, 'y': -33.5286, 'z': 1.85},
                    'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
    'associated_spaces': [
        {'id': '330', 'ifc_guid': '0x8tDwgKz4rBhuBSTQ03Vo', 'type': 'Space',
         'location': {'x': -5.15925, 'y': -33.5286, 'z': 7.85},
         'size': {'x': 9.799, 'y': 7.86, 'z': 3.7}}
    ],
    'associated_elements': [
        {'id': '396', 'ifc_guid': '26kn7MqLL9oOOTivXpgDH8', 'type': 'Wall',
         'location': {'x': -0.26, 'y': -33.5286, 'z': 1.85},
         'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
        {'id': '474', 'ifc_guid': '1T7BPQ_hn69uk5$Jp8cv99', 'type': 'Ceiling',
         'location': {'x': -5.15925, 'y': -33.5286, 'z': 3.7},
         'size': {'x': 9.799, 'y': 7.86, 'z': 0.0}, 'room': '330'},
        {'id': '707', 'ifc_guid': '0a$DTcOc10$eWx3Py5JFns', 'type': 'Floor',
         'location': {'x': -5.15925, 'y': -33.5286, 'z': 0.0},
         'size': {'x': 9.799, 'y': 7.86, 'z': 0.0}, 'room': '330'},
        {'id': '779', 'ifc_guid': '26kn7MqLL9oOOTivXpgCJg', 'type': 'Wall',
         'location': {'x': -5.15925, 'y': -29.5986, 'z': 1.85},
         'size': {'x': 9.799, 'y': 0.0, 'z': 3.7}, 'room': '330'},
        {'id': '792', 'ifc_guid': '1XD1GHfzD6cunMzxtqLi4o', 'type': 'Wall',
         'location': {'x': -10.0585, 'y': -33.5286, 'z': 1.85},
         'size': {'x': 0.0, 'y': 7.86, 'z': 3.7}, 'room': '330'},
        {'id': '818', 'ifc_guid': '26kn7MqLL9oOOTivXpgDiH,26kn7MqLL9oOOTivXpgDiH', 'type': 'Wall',
         'location': {'x': -5.15925, 'y': -37.4586, 'z': 1.85},
         'size': {'x': 9.799, 'y': 0.0, 'z': 3.7}, 'room': '330'},
    ]
}

result = plan_robot_task(user_info, robot_info, data)
print(result)
