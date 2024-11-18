from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from utils.loader import get_node_info
import json
client = OpenAI(
    api_key='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')

class NavigationPlan(BaseModel):
    path: List[int] = Field(..., description ='Path of rooms and doors to reach the defect node such as ["room id", "door id", "room id", "door id", "room id"] ')
    reasoning: str = Field(..., description ='Step-by-step reasoning for the decisions')


def get_navigationPath(defect_id: int, scene_graph, robots) -> tuple[List[int], str]:
    defect_node = get_node_info(defect_id)
    prompt = f"""
        You are an expert in navigation planning with graph data.

        Given the following information:
        1. Building information in 3D Scene Graph: {scene_graph} 
        3. robot information: {robots}

        Task:
        1. Plan possible and the most optimal path from robot's storage to the defect's location, which passes the least number of rooms and doors to the defect location.
            - Represent the path as a sequence of room_id and door_id in the format: [room_id, door_id, ... ].
        2. Final Output:
            - navigation_path: [room_id, door_id, room_id, door_id],
            - reasoning: Comprehensive step-by-step reasoning for all decisions made.
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
                "content": json.dumps(defect_node)
            }
        ],
        response_format=NavigationPlan,
        temperature=0,
        max_tokens=1000,
    )

    output = response.choices[0].message.parsed

    return output.path, output.reasoning


