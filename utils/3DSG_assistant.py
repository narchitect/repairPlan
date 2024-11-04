from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="3dscenegraph assistant",
    instructions="""You are a tool for retrieving node information from Scene Graph JSON.
       1. Extract all information about the requested node in JSON format
       2. Return only the JSON data without additional explanation
       3. If node is not found, return {"error": "Node not found"}""",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="3DSceneGraph")

file_paths = ["/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/3dsg_withCOR.json"]
file_streams = [open(path, "rb") for path in file_paths]

file_bath = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

print(file_bath.status)
print(file_bath.file_counts)

assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

message_file = client.files.create(
    file=open("/data/sceneGraphs/3dsg_withCOR.json", "rb"), purpose="assistants"
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "show me the room 8 info",
      # Attach the new file to the message.
      "attachments": [
        {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
      ],
    }
  ]
)

print(thread.tool_resources.file_search)

from typing_extensions import override
from openai import AssistantEventHandler, OpenAI




class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="show me the room 8 info.",
        event_handler=EventHandler(),
) as stream:
    stream.until_done()