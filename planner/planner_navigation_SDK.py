import json
import openai
import re


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
        - **Reasoning** Provide detailed reasoning for identifying this defect.
    2. Check reachability
        - Compare reach robot's max_reach_height with the defect location.
        - **Reachable Robots** List all robots reachable by this defect.
        - **Reasoning** Explain why each robot is considered reachable or not. 
    3. Final Output
        - Provide a JSON object with the following structure:
        {{
            "defect_node": "defect_node_id",
            "reachable_robots": ["robot_id", "robot_id", ...],
            "reasoning": "Comprehensive step-by-step reasoning for all decisions",
        }}
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
           - Provide a JSON object with the following structure:
             {{
               "defect_node": "defect_node_id",
               "defect_node_ifcGUID": "defect_node_ifcGUID",
               "reachable_accessible_robots": ["robot_id", "robot_id", ...],
               "navigation_path": ["room id", "door id", "room id", "door id", "room id"],
               "reasoning": "Comprehensive step-by-step reasoning for all decisions made."
             }}
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
    #stage1
    response_stage1 = openai.chat.completions.create(
        model="chatgpt-4o-latest",
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
        temperature=0.3,
        max_tokens= 1500,
    )

    full_response_stage1 = response_stage1.choices[0].message.content
    # print(full_response_stage1)
    json_output_stage1 = extract_json(full_response_stage1)
    # print(json_output_stage1)

    #stage2
    response_stage2 = openai.chat.completions.create(
        model="chatgpt-4o-latest",
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
        temperature=0.3,
        max_tokens=1500,
    )

    full_response_stage2 = response_stage2.choices[0].message.content
    # print(full_response_stage2)
    json_output_stage2 = extract_json(full_response_stage2)
    # print(json_output_stage2)

    return json_output_stage2


