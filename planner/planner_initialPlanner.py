from typing import Tuple, Any

from openai import OpenAI
from data_models import TaskData
from pydantic import BaseModel

client = OpenAI(
    api_key='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')


class InitialPlan(BaseModel):
    defect_id: int
    robot_id: int
    reasoning: str


def get_initialPlan(user_input, robot_db, scene_graph) -> tuple[int, int, str]:
    prompt = f"""
        You are an excellent graph search agent and an expert in building repairs with in-depth knowledge robot capabilities.

        Given the following information:
        Robot Database: {robot_db}
        Building information in 3D Scene Graphs: {scene_graph}

        Tasks:
        1. Identify the defect node in the 3D scene graph based on the user's description
        2. Select the best robot from the robot database to perform the repair task, considering its capability and reachability.
            - Compare the robot's max_reachable_height with the defect's location.

        Final output:
        1. Defect node id: the id of the defect node from 3D scene graph as integer 
        2. Robot node id: the id of the robot database as integer 
        3. Reasoning: Comprehensive step-by-step reasoning for all decisions made
        """

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
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
        response_format=InitialPlan,
        temperature=0,
        max_tokens=1000,
    )

    output = response.choices[0].message.parsed
    return output.defect_id, output.robot_id, output.reasoning
