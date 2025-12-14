import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found")

client = genai.Client(api_key=api_key)

MEMORY_FILE = "memory.json"

# Load memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

print("AI Chatbot started (type 'exit' to quit)")

chat = client.chats.create(model="gemini-2.5-flash")

while True:
    user_input = input("> ").strip()

    if user_input.lower() == "exit":
        print("Chatbot exited. Goodbye!")
        break

    if user_input.lower().startswith("my name is"):
        name = user_input[len("my name is"):].strip()
        memory["name"] = name

        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f)

        print(f"AI: Nice to meet you, {name}!")
        continue

    if user_input.lower() == "what is my name?":
        if "name" in memory:
            print(f"AI: Your name is {memory['name']}.")
        else:
            print("AI: You haven't told me your name yet.")
        continue

    response = chat.send_message(user_input)
    print("AI:", response.text)
