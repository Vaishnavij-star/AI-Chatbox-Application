import streamlit as st
import random
import datetime
import re
import pytz  # <-- Added for local timezone handling

# -------------------------------
# Initialize session state
# -------------------------------
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "rps_game" not in st.session_state:
    st.session_state.rps_game = None
if "guess_number" not in st.session_state:
    st.session_state.guess_number = None

# -------------------------------
# Hardcoded resources
# -------------------------------
tech_jokes = [
    "I told my computer I needed a break, and it said 'No problem, I’ll go to sleep.' 😆",
    "Why don’t programmers like nature? Too many bugs. 🐛",
    "Why do Java developers wear glasses? Because they don’t C#! 😎",
    "I would tell you a UDP joke, but you might not get it. 😂"
]

dad_jokes = [
    "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾🤣",
    "I told my wife she was drawing her eyebrows too high. She looked surprised. 😲",
    "Why did the math book look sad? Because it had too many problems. 📚",
    "I’m reading a book on anti-gravity. It’s impossible to put down! 😆"
]

one_liners = [
    "Parallel lines have so much in common… it’s a shame they’ll never meet. 😅",
    "I asked the elevator operator if he wanted to hear a joke. He said, 'Nah, I’m just here for the ups and downs.' 😄",
    "I told my boss I needed a raise because three companies were after me. He asked, 'Which companies?' I said, 'Electric, gas, and water.' 😎",
    "Why don’t skeletons fight each other? They don’t have the guts. 💀"
]

quotes = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Keep going. Be all in. – Bryan Hutchinson",
    "The best way to predict the future is to invent it. – Alan Kay",
    "Do something today that your future self will thank you for."
]

fun_facts = [
    "Honey never spoils. Archaeologists have found edible honey in 3000-year-old tombs!",
    "Bananas are berries, but strawberries are not!",
    "Octopuses have three hearts and blue blood.",
    "The Eiffel Tower can be 15 cm taller during hot days."
]

national_anthem = (
    "Jana Gana Mana Adhinayaka Jaya He\n"
    "Bharata Bhagya Vidhata\n"
    "Punjab Sindh Gujarat Maratha\n"
    "Dravida Utkala Banga\n"
    "Vindhya Himachala Yamuna Ganga\n"
    "Uchchhala Jaladhi Taranga\n"
    "Tava Subha Name Jage\n"
    "Tava Subha Ashish Mage\n"
    "Gahe Tava Jaya Gatha\n"
    "Jana Gana Mangaladayaka Jaya He\n"
    "Bharata Bhagya Vidhata\n"
    "Jaya He, Jaya He, Jaya He\n"
    "Jaya Jaya Jaya, Jaya He"
)

weather_data = {
    "mumbai": "Sunny 🌞, 32°C",
    "delhi": "Cloudy ☁️, 28°C",
    "kolkata": "Rainy 🌧️, 25°C",
    "bangalore": "Mild 🌤️, 27°C",
    "chennai": "Hot 🔥, 35°C"
}

# -------------------------------
# Chatbot response function
# -------------------------------
def get_response(user_input):
    text = user_input.lower().strip()
    tz = pytz.timezone("Asia/Kolkata")  # Local timezone
    now = datetime.datetime.now(tz)

    # ----------------- Greetings with current time -----------------
    if "my name" in text:
        return f"Your name is {st.session_state.username}. ✅"
    elif text.startswith(("hi", "hello", "hey")):
        hour = now.hour
        if hour < 12:
            tod = "Good morning ☀️"
        elif hour < 18:
            tod = "Good afternoon 🌤️"
        else:
            tod = "Good evening 🌙"
        current_time = now.strftime("%H:%M")
        return f"{tod}, {st.session_state.username}! 👋 It's {current_time} now."
    elif "how r u" in text or "how are you" in text:
        return "I'm great! 😊 How about you?"

    # ----------------- Jokes with categories -----------------
    if "joke" in text:
        if "tech" in text:
            return random.choice(tech_jokes)
        elif "dad" in text:
            return random.choice(dad_jokes)
        elif "one-liner" in text or "one liner" in text:
            return random.choice(one_liners)
        else:
            all_jokes = tech_jokes + dad_jokes + one_liners
            return random.choice(all_jokes)

    # ----------------- Time/Date -----------------
    if "time" in text:
        return f"The current time is {now.strftime('%H:%M')} ⏰"
    if "date" in text or "day" in text:
        return f"Today is {now.strftime('%A, %B %d, %Y')} 📅"

    # ----------------- National anthem -----------------
    if "national anthem" in text:
        return national_anthem

    # ----------------- Mood-based songs -----------------
    if "song" in text or "mood" in text:
        if "happy" in text:
            songs = ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake", "Good Feeling - Flo Rida"]
        elif "sad" in text:
            songs = ["Someone Like You - Adele", "Fix You - Coldplay", "Stay With Me - Sam Smith"]
        elif "love" in text or "romantic" in text:
            songs = ["Perfect - Ed Sheeran", "All of Me - John Legend", "Thinking Out Loud - Ed Sheeran"]
        elif "energetic" in text or "workout" in text:
            songs = ["Eye of the Tiger - Survivor", "Stronger - Kanye West", "Thunderstruck - AC/DC"]
        elif "chill" in text or "relax" in text:
            songs = ["Sunflower - Post Malone", "Lose You To Love Me - Selena Gomez", "Ocean Eyes - Billie Eilish"]
        else:
            songs = ["Shape of You - Ed Sheeran", "Blinding Lights - The Weeknd", "Levitating - Dua Lipa"]
        return "Here are some songs you can listen to:\n- " + "\n- ".join(songs)

    # ----------------- Quotes / Fun Facts -----------------
    if "inspire" in text or "motivate" in text:
        return random.choice(quotes)
    if "fun fact" in text or "fact" in text:
        return random.choice(fun_facts)

    # ----------------- Simple math -----------------
    math_match = re.match(r"what is (\d+)\s*([+\-*/])\s*(\d+)", text)
    if math_match:
        a, op, b = math_match.groups()
        a, b = int(a), int(b)
        if op == "+": return f"{a} + {b} = {a+b}"
        if op == "-": return f"{a} - {b} = {a-b}"
        if op == "*": return f"{a} * {b} = {a*b}"
        if op == "/": return f"{a} / {b} = {a/b:.2f}"

    # ----------------- Weather -----------------
    if "weather" in text:
        for city in weather_data:
            if city in text:
                return f"{city.capitalize()}: {weather_data[city]}"
        return "Sorry, I only know weather for Mumbai, Delhi, Kolkata, Bangalore, Chennai 🌤️"

    # ----------------- Games -----------------
    # Rock-Paper-Scissors
    if "rock-paper-scissors" in text or "play rps" in text:
        st.session_state.rps_game = True
        return "Let's play Rock-Paper-Scissors! Type your move: rock, paper, or scissors."
    if st.session_state.rps_game and text in ["rock", "paper", "scissors"]:
        bot_move = random.choice(["rock", "paper", "scissors"])
        result = "It's a tie! 🤝" if text == bot_move else \
                 "You win! 🎉" if (text=="rock" and bot_move=="scissors") or \
                                 (text=="paper" and bot_move=="rock") or \
                                 (text=="scissors" and bot_move=="paper") else "You lose! 😢"
        st.session_state.rps_game = None
        return f"Bot chose {bot_move}. {result}"

    # Number guessing game
    if "play number guessing" in text:
        st.session_state.guess_number = random.randint(1, 20)
        return "I have thought of a number between 1 and 20. Try to guess it!"
    if st.session_state.guess_number:
        try:
            guess = int(text)
            if guess < st.session_state.guess_number:
                return "Too low! Try again."
            elif guess > st.session_state.guess_number:
                return "Too high! Try again."
            else:
                st.session_state.guess_number = None
                return "Correct! 🎉 You guessed my number."
        except:
            return "Please enter a valid number between 1 and 20."

    # ----------------- Fallback -----------------
    return f"You said: {user_input}"

# -------------------------------
# Streamlit App
# -------------------------------
st.title("🧪 Vaishnavi's Ultimate Offline Chatbot")
st.write("100% offline – jokes, songs, games, quotes, weather, time, and more!")

# --- Name input ---
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

# --- Chat input ---
if st.session_state.username != "" and st.session_state.greeted:
    user_input = st.text_input(f"{st.session_state.username}, type your message:", key="chat_input")
    if st.button("Send") and user_input.strip() != "":
        st.session_state.chat_history.append({"sender": "You", "message": user_input})
        response = get_response(user_input)
        st.session_state.chat_history.append({"sender": "Bot", "message": response})

# --- Display chat history ---
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
