import streamlit as st
import random
import datetime

# -------------------------------
# Initialize session state
# -------------------------------
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False  # Ensures greeting only once

# -------------------------------
# Chatbot response function
# -------------------------------
def get_response(user_input):
    text = user_input.lower().strip()
    if "my name" in text:
        return f"Your name is {st.session_state.username}. ✅"
    elif text.startswith(("hi", "hello", "hey")):
        return f"Hello {st.session_state.username}! 👋"
    elif "how r u" in text or "how are you" in text:
        return "I'm great! 😊 How about you?"
    elif "joke" in text:
        jokes = [
            "Why did the Python programmer wear glasses? Because they couldn't C#! 😎",
            "Why do programmers prefer dark mode? Because light attracts bugs! 😆",
            "Why was the JavaScript developer sad? Because they didn’t know how to 'null' their feelings 😂",
            "Why did the computer show up at work late? It had a hard drive! 🤣"
        ]
        return random.choice(jokes)
    elif "time" in text:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M')} ⏰"
    elif "date" in text or "day" in text:
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')} 📅"
    else:
        return f"You said: {user_input}"

# -------------------------------
# Streamlit App
# -------------------------------
st.title("Vaishnavi's AI Chatbot 🤖")

# --- Step 1: Name input ---
if st.session_state.username == "":
    name_input = st.text_input("Hi! What's your name?", key="name_input")
    if st.button("Submit Name"):
        if name_input.strip() != "":
            st.session_state.username = name_input.strip()
            if not st.session_state.greeted:
                st.session_state.chat_history.append(
                    {"sender": "Bot", "message": f"Hello {st.session_state.username}! 👋 Nice to meet you."}
                )
                st.session_state.greeted = True

# --- Step 2: Chat input ---
if st.session_state.username != "" and st.session_state.greeted:
    user_input = st.text_input(f"{st.session_state.username}, type your message:", key="chat_input")
    if st.button("Send") and user_input.strip() != "":
        # Append user message
        st.session_state.chat_history.append({"sender": "You", "message": user_input})
        # Append bot response
        response = get_response(user_input)
        st.session_state.chat_history.append({"sender": "Bot", "message": response})

# --- Step 3: Display chat history with colored bubbles ---
for chat in st.session_state.chat_history:
    if chat["sender"] == "You":
        st.markdown(
            f"<div style='text-align: right; background-color: #DCF8C6; color: black; padding:10px; border-radius:10px; margin:5px 0;'>{chat['message']}</div>", 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align: left; background-color: #4B4B4B; color: white; padding:10px; border-radius:10px; margin:5px 0;'>{chat['message']}</div>", 
            unsafe_allow_html=True
        )
