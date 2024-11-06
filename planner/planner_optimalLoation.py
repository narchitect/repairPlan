from openai import OpenAI
import json

# Set your OpenAI API key
client = OpenAI(api_key='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')


# Function to find the optimal scanning location
def find_optimal_location(env_data, camera_fov):

    system = """You are an assistant specializing in robot action planning and environment analysis. 
    Your task is to help determine the optimal scanning location for a robot to inspect defects within a building environment. 
    Consider factors such as the robot's field of view, environmental obstacles, and the defect's location when providing calculations and recommendations."""

    # Prepare the prompt for OpenAI API
    prompt = f"""
    Given the environment data and a camera with {camera_fov} degrees Field of View (FOV), find the optimal location to scan the defect object.
    
    Note: The "location" of each object represents the central point coordinate of that object.
    
    Environment Data:
    - Defect Node: {env_data['defect_node']}
    - Associated Spaces: {env_data['associated_spaces']}
    - Associated Elements: {env_data['associated_elements']}
    
    Important
    the location key in nodes are central coordinate of the object. 
    
    Please provide the reasoning steps as a chain of thought, include the formulas used, and finally output the optimal location in JSON format as:
    optimal_location = {{'x': x_value, 'y': y_value, 'z': z_value}}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2500,
        temperature=0,
    )

    full_response = response.choices[0].message.content

    return full_response

