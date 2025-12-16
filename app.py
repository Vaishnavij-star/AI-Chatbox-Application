import streamlit as st
import random
import datetime
import re
import pytz
import string  # for punctuation removal

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

riddles = [
    "I speak without a mouth and hear without ears. What am I? 🤔",
    "I’m tall when I’m young, and I’m short when I’m old. What am I? 🕯️",
    "What has keys but can’t open locks? 🔑",
    "What can travel around the world while staying in a corner? 🌍"
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
    # Normalize fancy quotes
    user_input = user_input.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    # Remove surrounding quotes
    user_input = user_input.strip('"').strip("'")
    # Lowercase and remove punctuation (except /, +, -, *)
    text = user_input.lower().strip()
    text_clean = text.translate(str.maketrans('', '', string.punctuation.replace("/", "").replace("+","").replace("-","").replace("*","")))

    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)

    # ----------------- Greetings -----------------
    if "my name" in text_clean:
        return f"Your name is {st.session_state.username}. ✅"
    elif text_clean.startswith(("hi", "hello", "hey")):
        hour = now.hour
        tod = "Good morning ☀️" if hour < 12 else "Good afternoon 🌤️" if hour < 18 else "Good evening 🌙"
        current_time = now.strftime("%H:%M")
        return f"{tod}, {st.session_state.username}! 👋 It's {current_time} now."
    elif "how r u" in text_clean or "how are you" in text_clean:
        return "I'm great! 😊 How about you?"

    # ----------------- Jokes -----------------
    if "joke" in text_clean:
        if "tech" in text_clean:
            return random.choice(tech_jokes)
        elif "dad" in text_clean:
            return random.choice(dad_jokes)
        elif "one-liner" in text_clean or "one liner" in text_clean:
            return random.choice(one_liners)
        else:
            return random.choice(tech_jokes + dad_jokes + one_liners)

    # ----------------- Riddles -----------------
    if "riddle" in text_clean:
        return random.choice(riddles)

    # ----------------- National anthem -----------------
    if "national anthem" in text_clean or "anthem" in text_clean:
        return national_anthem

    # ----------------- Songs / Mood -----------------
    if "song" in text_clean or "mood" in text_clean:
        if "happy" in text_clean:
            songs = ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake", "Good Feeling - Flo Rida"]
        elif "sad" in text_clean:
            songs = ["Someone Like You - Adele", "Fix You - Coldplay", "Stay With Me - Sam Smith"]
        elif "love" in text_clean or "romantic" in text_clean:
            songs = ["Perfect - Ed Sheeran", "All of Me - John Legend", "Thinking Out Loud - Ed Sheeran"]
        elif "energetic" in text_clean or "workout" in text_clean:
            songs = ["Eye of the Tiger - Survivor", "Stronger - Kanye West", "Thunderstruck - AC/DC"]
        elif "chill" in text_clean or "relax" in text_clean:
            songs = ["Sunflower - Post Malone", "Lose You To Love Me - Selena Gomez", "Ocean Eyes - Billie Eilish"]
        else:
            songs = ["Shape of You - Ed Sheeran", "Blinding Lights - The Weeknd", "Levitating - Dua Lipa"]
        return "Here are some songs you can listen to:\n- " + "\n- ".join(songs)

    # ----------------- Quotes / Fun Facts -----------------
    if "inspire" in text_clean or "motivate" in text_clean:
        return random.choice(quotes)
    if "fun fact" in text_clean or "fact" in text_clean:
        return random.choice(fun_facts)

    # ----------------- Time / Date -----------------
    if "time" in text_clean:
        return f"The current time is {now.strftime('%H:%M')} ⏰"
    if "date" in text_clean or "day" in text_clean:
        return f"Today is {now.strftime('%A, %B %d, %Y')} 📅"

    # ----------------- Simple Math -----------------
    math_text = text_clean.rstrip("?")
    math_match = re.match(r"what is (\d+)\s*([+\-*/])\s*(\d+)", math_text)
    if math_match:
        a, op, b = math_match.groups()
        a, b = int(a), int(b)
        if op == "+": return f"{a} + {b} = {a+b}"
        if op == "-": return f"{a} - {b} = {a-b}"
        if op == "*": return f"{a} * {b} = {a*b}"
        if op == "/": return f"{a} / {b} = {a/b:.2f}"

    # ----------------- Weather -----------------
    if "weather" in text_clean:
        for city in weather_data:
            if city in text_clean:
                return f"{city.capitalize()}: {weather_data[city]}"
        return "Sorry, I only know weather for Mumbai, Delhi, Kolkata, Bangalore, Chennai 🌤️"

    # ----------------- Games -----------------
    text_rps = text_clean.replace('"', '').replace("'", "")
    if "rock-paper-scissors" in text_rps or "play rps" in text_rps:
        st.session_state.rps_game = True
        return "Let's play Rock-Paper-Scissors! Type your move: rock, paper, or scissors."

    if st.session_state.rps_game:
        move = text_rps
        if move in ["rock", "paper", "scissors"]:
            bot_move = random.choice(["rock", "paper", "scissors"])
            result = "It's a tie! 🤝" if move == bot_move else \
                     "You win! 🎉" if (move=="rock" and bot_move=="scissors") or \
                                     (move=="paper" and bot_move=="rock") or \
                                     (move=="scissors" and bot_move=="paper") else "You lose! 😢"
            st.session_state.rps_game = None
            return f"Bot chose {bot_move}. {result}"

    if "play number guessing" in text_clean:
        st.session_state.guess_number = random.randint(1, 20)
        return "I have thought of a number between 1 and 20. Try to guess it!"

    if st.session_state.guess_number:
        try:
            guess = int(text_clean)
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

# --- Chat input using form ---
if st.session_state.username != "" and st.session_state.greeted:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(f"{st.session_state.username}, type your message:")
        submit_button = st.form_submit_button("Send")
        if submit_button and user_input.strip() != "":
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
