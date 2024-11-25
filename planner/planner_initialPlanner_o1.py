from typing import Tuple, Any, Optional
from openai import OpenAI
from pydantic import BaseModel
from utils.loader import get_node_info, extract_json


client = OpenAI(
    api_key='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')

def identify_defect_node(user_input: str, scene_graph: Any) -> Tuple[Optional[int]]:
    scene_graph_nodes = scene_graph["nodes"]
    prompt = f"""
    You are an expert in building repairs with extensive knowledge of 3D scene graphs.

    Based on the following information:
    - Building information in 3D Scene Graphs: {scene_graph_nodes}
    - User input: {user_input}

    Task:
    - Identify the defect node in the 3D scene graph using the user's description.
    - Identify the room node where the defect node is located.
    - If you find several suspicious defects based on the user's description, generate specific clarifying questions to specify the defects among them.

    Final output should be in JSON format:
    {{
        "Defect_id": integer defect node id or null,
        "Room_id": integer room node id where defect node is located, null
        "Questions": string with your questions or null 
    }}
    """

    # Initial attempt to identify the defect node
    response = client.chat.completions.create(
        model="o1-preview",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    # Parse the assistant's response
    output = response.choices[0].message.content
    print(output)

    output_json = extract_json(output)

    if output_json['Defect_id'] is not None and output_json['Questions'] is None:
        return output_json['Defect_id'], output_json['Room_id']
    
    else:
        if output_json['Questions']:
            # Get user's answers
            user_answers = input(f"{output_json['Questions']} your answer:")

            # Combine original user input with new answers
            combined_input = f"{user_input}\nAdditional Information: user_answer{user_answers}"

            # Retry identification with the new information
            return identify_defect_node(combined_input, scene_graph)
        else:
            # Unable to identify and no questions generated
            print("Unable to identify the defect node based on the provided information.")
            print(output)
            return None, None

def select_robot(user_input, defect_id, robot_db) -> tuple[Any, Any]:
    defect_info = get_node_info(defect_id)

    prompt = f"""
    You are an expert in robot capabilities and reachability.
    
    Given the following information:
    Defect node id: {defect_info}
    Robot Database: {robot_db}
    user_input: {user_input}
    
    Task:
    Select the best robot from the robot database to perform the repair task, considering its capability and reachability.
    Compare the robot's max_reachable_height with the defect's location.
    
    Final output should be in JSON format:
    {{
        "Robot_id": integer robot node id
    }}
    """

    response = client.chat.completions.create(
        model="o1-preview",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    output = response.choices[0].message.content
    print(output)
    output_json = extract_json(output)
    return output_json['Robot_id']