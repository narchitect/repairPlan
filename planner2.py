import json
import openai
from pydantic import BaseModel
from typing import List

class selected_robots(BaseModel):
    reachable_robots: List[str]
    accessible_robots: List[str]
    reachableAndAccessible_robots: List[str]

class NavigationPath(BaseModel):
    path: List[str]
def load_scene_graph(file_path):
    with open(file_path, 'r') as f:
        scene_graph = json.load(f)
    return scene_graph
def generate_prompt(scene_graph, robots):
    prompt = f"""
        You are an expert in building repairs and navigation, with in-depth knowledge of various robot capabilities.

        3D Scene Graph:
        Here is a 3D scene graph representation of the environment:
        {scene_graph}

        Robots Available:
        {robots}

        Tasks:
        1. **Identify Defect**:**
           - Analyze the user's defect description 
           - identify the target defect node within the 3D scene graph.
           - **Reasoning:** Provide detailed reasoning for identifying this defect.

        2. **Check Reachability:**
           - Compare each robot's `max_reach_height` with the defect location's height.
           - **Reachable Robots:** List all robots that can reach the defect.
           - **Reasoning:** Explain why each robot is considered reachable or not.

        3. **Generate Navigation Paths:**
           - Create possible and optimal navigation path to the defect location.
           - Represent the path as a sequence of `room_id` and `door_id` in the format: `[room1, door1, room2, door2, ..., roomN]`.
           - Extract and list all doors present in each path.
           - **Reasoning:** Describe how you constructed each navigation path.


        4. **Check Accessibility:**
           - For the navigation path, compare the door sizes with each robot's size to determine accessibility.
           - **Reasoning:** Explain the accessibility assessment for each robot through the doors.
           - **Accessible Robots:** List robots that can access through the doors on the path.
           - If no robots can access a path, regenerate the navigation path until at least one robot can access.

        5. **Final Output:**
           - Provide a JSON object with the following structure:
             {{
               "defect_node": "defect_object_name",
               "selected_robots": ["robot_name1", "robot_name2", ...],
               "navigation_paths": [
                   {{
                       "path": ["room1", "door1", "room2", "door2", "room3"],
                       "doors": ["door1", "door2"],
                       "reachable_robots": ["robot1", "robot2", "robot3"],
                       "accessible_robots": ["robot1", "robot3"]
                   }},
               ],
               "reasoning": "Comprehensive step-by-step reasoning for all decisions made."
             }}

        **Constraints:**
        - Ensure that the selected robots have the necessary actions to address the defect.
        - Maintain clear and logical reasoning for each step.
        - Structure your response by first detailing your reasoning for each task, followed by the final JSON output.
        
        **Example Format:**
        1. **Identify Defect:**
           - Reasoning: [Your detailed reasoning here.]
        
        2. **Check Reachability:**
           - Reasoning: [Your detailed reasoning here.]

        ...
        
         **Final Output:**
        ```json
        {{
          "defect_node": "defect_object_name",
          "selected_robots": ["robot_name1", "robot_name2"],
          "navigation_paths": [
            {{
              "path": ["room1", "door1", "room2", "door2", "room3"],
              "doors": ["door1", "door2"],
              "accessible_robots": ["robot1", "robot3"]
            }}
          ],
          "reasoning": "Comprehensive step-by-step reasoning for all decisions made."
        }}"""
    return prompt


def get_navigation_plan(user_input, scene_graph, robots):
    prompt_template = generate_prompt(scene_graph, robots)
    system_prompt = prompt_template
    user_message = user_input

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.3,
        max_tokens=2500
    )

    full_response = response.choices[0].message.content

    # # Extract the JSON part from the response
    # json_pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
    # match = json_pattern.search(full_response)
    #
    # if match:
    #     json_str = match.group(1)
    #     try:
    #         navigation_plan = json.loads(json_str)
    #     except json.JSONDecodeError:
    #         navigation_plan = {"error": "Failed to parse JSON response from LLM."}
    # else:
    #     navigation_plan = {"error": "JSON block not found in the response."}
    #
    # # Optionally, extract reasoning if needed
    # reasoning_pattern = re.compile(r'(\d+\.\s\*\*.*?:\s*-\s*Reasoning:.*)', re.DOTALL)
    # reasoning_match = reasoning_pattern.findall(full_response)
    # reasoning = "\n".join(reasoning_match) if reasoning_match else "No reasoning found."

    # Return both navigation plan and reasoning
    return full_response


