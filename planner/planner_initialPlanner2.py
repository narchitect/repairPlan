from typing import Tuple, Any, Optional
from openai import OpenAI
from pydantic import BaseModel
from utils.loader import get_node_info


client = OpenAI(
    api_key='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')

class RobotSelection(BaseModel):
    robot_id: int
    reasoning: str

class DefectIdentification(BaseModel):
    defect_id: Optional[int] = None
    reasoning: Optional[str] = None
    questions: Optional[str] = None

def identify_defect_node(user_input: str, scene_graph: Any) -> Tuple[Optional[int], Optional[int], str]:

    prompt = f"""
    You are an expert in building repairs with extensive knowledge of 3D scene graphs.

    Given the following information:
    Building information in 3D Scene Graphs: {scene_graph}

    Task:
    Identify the defect node in the 3D scene graph based on the user's description.
    If you cannot confidently identify the defect node, generate relevant clarifying questions to ask the user.
    for example, user mention an element in a room but there are several elements with same types, then you can make a question to indentify specific element.
    if you can identify the defect node, return questions as None.

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
        response_format=DefectIdentification,
        temperature=0,
        max_tokens=500,
    )

    # Parse the assistant's response
    output = response.choices[0].message.parsed

    print(output)

    if output.defect_id is not None and output.questions is None:
        # Retrieve room_id if defect_id is available
        defect_id = output.defect_id
        room_id = get_node_info(defect_id)["room"]
        reasoning = output.reasoning
        # Defect node identified
        return defect_id, room_id, reasoning
    else:
        if output.questions:
            # Ask the user for more information
            print("I need more information to identify the defect. Please answer the following questions:")
            print(output.questions)
            # Get user's answers
            user_answers = input("Your answers: ")

            # Combine original user input with new answers
            combined_input = f"{user_input}\nAdditional Information: question:{output.questions} user_answer{user_answers}"

            # Retry identification with the new information
            return identify_defect_node(combined_input, scene_graph)
        else:
            # Unable to identify and no questions generated
            print("Unable to identify the defect node based on the provided information.")
            return None, None, output.reasoning

def select_robot(user_input, defect_id, robot_db) -> tuple[Any, Any]:
    defect_info = get_node_info(defect_id)

    prompt = f"""
    You are an expert in robot capabilities and reachability.
    
    Given the following information:
    Defect node id: {defect_info}
    Robot Database: {robot_db}
    
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
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        response_format=RobotSelection,
        temperature=0,
        max_tokens=2000,
    )

    output = response.choices[0].message.parsed
    return output.robot_id, output.reasoning
