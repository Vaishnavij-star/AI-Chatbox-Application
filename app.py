import streamlit as st
import json
import os
import random

# ---------------- MEMORY (persistent) ----------------
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

memory = load_memory()

# ---------------- SESSION CHAT HISTORY ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- UI ----------------
st.set_page_config(page_title="Vaishnavi's AI Chatbot", page_icon="🤖")
st.title("Vaishnavi's AI Chatbot 🤖")

# ---------------- INTENT DETECTION ----------------
def detect_intent(text):
    text = text.lower()

    if text.startswith("my name is"):
        return "set_name"
    if "what's my name" in text or "whats my name" in text:
        return "get_name"
    if any(word in text for word in ["hi", "hello", "hey"]):
        return "greeting"
    if "joke" in text:
        return "joke"
    if any(word in text for word in ["thanks", "thank you"]):
        return "thanks"
    if "help" in text:
        return "help"
    
    return "fallback"

# ---------------- RESPONSES ----------------
jokes = [
    "Why don’t programmers like nature? It has too many bugs 😄",
    "Why did the computer go to therapy? Because it had too many crashes 🤯",
    "Why was the JavaScript developer sad? Because they didn’t know how to 'null' their feelings 😂"
]

fallback_responses = [
    "Hmm 🤔 that’s interesting!",
    "Tell me more!",
    "I’m still learning — can you explain that?",
    "Let’s talk about something fun 😄"
]

# ---------------- CHAT DISPLAY ----------------
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.chat_history.append(("user", user_input))

    intent = detect_intent(user_input)

    # ---------------- AI LOGIC ----------------
    if intent == "set_name":
        name = user_input[11:].strip()
        memory["name"] = name
        save_memory(memory)
        ai_response = f"Nice to meet you, {name}! 😊"

    elif intent == "get_name":
        if "name" in memory:
            ai_response = f"Your name is {memory['name']}. ✅"
        else:
            ai_response = "I don't know your name yet. Type **My name is ...**"

    elif intent == "greeting":
        if "name" in memory:
            ai_response = f"Hello {memory['name']}! 👋"
        else:
            ai_response = "Hello! 👋 What’s your name?"

    elif intent == "joke":
        ai_response = random.choice(jokes)

    elif intent == "thanks":
        ai_response = "You're welcome! 😊"

    elif intent == "help":
        ai_response = (
            "I can:\n"
            "- Remember your name\n"
            "- Tell jokes 😄\n"
            "- Chat with you\n\n"
            "Try typing **Tell me a joke** or **What's my name?**"
        )

    else:
        ai_response = random.choice(fallback_responses)

    # Show AI response
    st.session_state.chat_history.append(("assistant", ai_response))

    # Rerun to update UI
    st.rerun()
