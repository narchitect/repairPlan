from typing import Tuple, Any, Optional
from openai import OpenAI
from pydantic import BaseModel
from utils.loader import get_node_info


client = OpenAI(
    api_key='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')


def identify_defect_node(user_input: str, scene_graph: Any) -> Tuple[Optional[int], Optional[int], str]:

    prompt = f"""
    You are an expert in building repairs with extensive knowledge of 3D scene graphs.

    Given the following information:
    Building information in 3D Scene Graphs: {scene_graph}
    user_input: {user_input}

    Task:
    Identify the defect node in the 3D scene graph based on the user's description.
    If you cannot confidently identify the defect node, generate relevant clarifying questions to ask the user.
    for example, you find the same type surfaces in the room user mention, but you don't have enough information to identify the defect among them,
    then you can ask the user to provide more information about the defect.

    Final output:
    "defect_id": [defect_id as integer or null],
    "reasoning": "Your reasoning for indentifying defects.",
    "questions": "Your questions here (if any, if not, set it as None)."
    """

    # Initial attempt to identify the defect node
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
    )

    # Parse the assistant's response
    output = response.choices[0].message.content

    print(output)
    return output



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
    
    Final output:
    1. Robot node id: the id of the robot database as integer
    2. Reasoning: Comprehensive step-by-step reasoning for all decisions made
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    output = response.choices[0].message.content
    print(output)
    return output
