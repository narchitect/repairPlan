from transformers import GPT2Tokenizer

# Initialize the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Read the file
file_path = "data/sceneGraphs/new_structure/3dsg_full.json"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Count the tokens in the file content
tokens = tokenizer.encode(content)
token_count = len(tokens)
print("Token count:", token_count)
