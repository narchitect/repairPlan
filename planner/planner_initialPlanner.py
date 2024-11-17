import json
from openai import OpenAI
import re
from pydantic import BaseModel, Field
from typing import List, Union

client = OpenAI(
    api_key='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')

class Room(BaseModel):
    room_id: int = Field(..., description="Unique identifier for the room")
class Door(BaseModel):
    door_id: int = Field(..., description="Unique identifier for the door")
class Stage2_output(BaseModel):
    defect_node: int = Field(..., description='ID of the defect node')
    defect_node_ifcGUID: str = Field(..., description ='GUID of the defect node in IFC format')
    reachable_accessible_robots: List[int] = Field(..., description ='List of IDs of robots that can access the defect node')
    navigation_path: List[Union[Room, Door]] = Field(..., description ='Path of rooms and doors to reach the defect node such as ["room id", "door id", "room id", "door id", "room id"] ')
    reasoning: str = Field(..., description ='Step-by-step reasoning for the decisions')

class Stage1_output(BaseModel):
    defect_node: int = Field(..., description='ID of the defect node')
    reachable_robots: List[int] = Field(..., description = "List of IDs of robots that can reach the defect node")
    reasoning: str = Field(..., description ='Step-by-step reasoning for the decisions')

def initialPlan_stage1(user_input, scene_graph, robots):
    prompt = f"""
    You are an excellent graph search agent and an expert in building repairs and navigation, with in-depth knowledge robot capabilities.
    User's description on the defect:
    {user_input}
    3D Scene Graph:
    Here is a 3D scene graph representation of the environment:
    {scene_graph}
    Robots Available:
    {robots}
    Tasks:
    1. Identify Defect
        - Identify the target defect node within the 3d scene graph by analyzing the user's defect description.
    2. Check reachability
        - Compare reach robot's max_reach_height with the defect location.
        - **Reachable Robots** List all robots reachable by this defect.
    3. Final Output
        - Provide an output with the following structure:
            "defect_node": "defect_node_id",
            "reachable_robots": ["robot_id", "robot_id", ...],
            "reasoning": "Comprehensive step-by-step reasoning for all decisions",
    """
    return prompt
def initialPlan_stage2(robot_location):
    prompt = f"""
        You are continuing from the previous analysis.

        Current robot location:
        {robot_location}
        based on the previous response and current robot location, generate the plan for the task below:
        
        1. Generate Navigation Paths
            - Create possible and the most optimal path which passes the least number of rooms and doors to the defect location.
            - Represent the path as a sequence of room_id and door_id in the format: [room_id, door_id, ... ].
            - **Doors** Extract and list all doors present in the path in the format [door_id, door_id, ...]. 
            - **Reasoning** Describe how you constructed the navigation path. 

        1. **Check Accessibility:**
           - For the navigation path, compare the door sizes (width and height) with each robot's size to determine accessibility from reachable robots.
           - **Accessible Robots:** List robots that can access through the doors on the path.
           - **Reasoning:** Explain the accessibility assessment for each robot through the doors.
           - If no robots can access a path, regenerate the navigation path until at least one robot can access.

        2. **Final Output:**
           - Provide an output with the following structure:
               "defect_node": "defect_node_id",
               "defect_node_ifcGUID": "defect_node_ifcGUID",
               "reachable_accessible_robots": ["robot_id", "robot_id", ...],
               "navigation_path": ["room id", "door id", "room id", "door id", "room id"],
               "reasoning": "Comprehensive step-by-step reasoning for all decisions made."
    """
    return prompt

def extract_json(response_content):
    # Extract the JSON part from the response using regex
    json_match = re.search(r'```json\n(.*?)\n```', response_content, re.DOTALL)
    if json_match:
        json_output = json_match.group(1)
        try:
            return json.loads(json_output)  # Parse and return the JSON content
        except json.JSONDecodeError:
            print("An error occurred while parsing the json response")
            return None
    else:
        print("Can't find the JSON output section")
        return None


def get_inspectionPlan(user_input, scene_graph, robots, robot_location):
    final_output = []
    #stage1
    response_stage1 = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": initialPlan_stage1(user_input, scene_graph, robots)
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        response_format= Stage1_output,
        temperature=0,
        max_tokens= 2000,
    )

    full_response_stage1 = response_stage1.choices[0].message.content
    # print(full_response_stage1)
    stage1_output = response_stage1.choices[0].message.parsed
    # print(stage_output)
    final_output.append(stage1_output)

    #stage2
    response_stage2 = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": initialPlan_stage2(robot_location)
            },
            {
                "role": "user",
                "content": user_input
            },
            {
                "role": "assistant",
                "content": full_response_stage1
            }
        ],
        response_format= Stage2_output,
        temperature=0,
        max_tokens=2000,
    )

    full_response_stage2 = response_stage2.choices[0].message.content
    # print(full_response_stage2)
    stage2_output = response_stage2.choices[0].message.parsed
    # print(json_output_stage2)
    final_output.append(stage2_output)

    return final_output


