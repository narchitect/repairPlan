from openai import OpenAI
import json

# OpenAI API Key setup
client = OpenAI(api_key = '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')

# Load the trimmed and full 3D Scene Graphs
with open('../data/sceneGraphs/3dsg_withIds.json') as trimmed_file:
    trimmed_3dsg = json.load(trimmed_file)

with open('../data/sceneGraphs/full_3dsg.json') as full_file:
    full_3dsg = json.load(full_file)

messages = []
messages.append({"role": "system", "content": "You are an assistant to identify defects in a 3D scene graph."})
messages.append({"role": "user", "content": f"Here is a 3D scene graph of the building: {trimmed_3dsg}"})

# Function to find defect node based on user instruction
def find_defect_node(user_description):
    messages.append({"role": "user", "content": f"Identify the defect object ID and room ID based on the user description: {user_description}"})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=[
            {
                "name": "get_defect_info",
                "description": "Returns the defect object ID and room ID based on the user's defect description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "defect_object_id": {
                            "type": "string",
                            "description": "The ID of the defect object"
                        },
                        "room_id": {
                            "type": "string",
                            "description": "The ID of the room where the defect is located"
                        }
                    },
                    "required": ["defect_object_id", "room_id"]
                }
            }
        ],
        function_call="auto"
    )

    if response.choices[0].finish_reason == "function_call":
        function_call = response.choices[0].message.function_call
        if function_call.name == "get_defect_info":
            defect_info = json.loads(function_call.arguments)
            return defect_info.get("defect_object_id"), defect_info.get("room_id")
    return None, None


# Function to retrieve full information of a defect node from full_3dsg
def retrieve_node_info(node_id):
    for category in ["spaces", "components", "elements"]:
        for node in full_3dsg.get(category, []):
            if node["id"] == node_id:
                return node
    return None

def get_defect_and_room_info(defect_object_id, room_id):
    defect_info = retrieve_node_info(defect_object_id)
    room_info = retrieve_node_info(room_id)
    return {
        "defect_info": defect_info,
        "room_info": room_info
    }




# Find defect node IDs based on user description
defect_object_id, room_id = find_defect_node(user_description)
if defect_object_id and room_id:
    print(f"Defect Object ID: {defect_object_id}, Room ID: {room_id}")

    # Retrieve full information about the defect node
    node_info = get_defect_and_room_info(defect_object_id, room_id)
    print(node_info)

    # Send the detailed node information back to GPT for further processing if needed
    # if node_info:
    #     follow_up_response = openai.ChatCompletion.create(
    #         model="gpt-4-0613",
    #         messages=[
    #             {"role": "system", "content": "Process the detailed information of a defect node."},
    #             {"role": "user",
    #              "content": f"Here is the full information for node {defect_object_id}: {json.dumps(node_info)}"}
    #         ]
    #     )
    #     print("GPT's follow-up response:", follow_up_response.choices[0].message["content"])
else:
    print("Unable to locate the defect node based on the description.")
