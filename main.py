import streamlit as st

# Configure streamlit front page
st.set_page_config(
    page_title = "Personal Voice Assistant",
    layout  = 'wide'
)

# import other libraries
import os      # to get path of env variable
import time    # set the timer for listen
import pyttsx3  # convert text to speech
import speech_recognition as sr  # convert speech to text
from groq import Groq   # API key to use LLM service
from dotenv import load_dotenv  # to load API key from system

# load the API key inside code
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Checking if API key is set or not
if not GROQ_API_KEY:
    st.error("Missing API key")
    st.stop()

# Configure the LLM
client = Groq(api_key = GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

# Initialize speech to text recognizer
recognizer = sr.Recognizer

# Inititalize Text to Speech engine
def get_tts_engine():
    try:
        engine = pyttsx3.init()
        return engine
    except Exception as e:
        st.error("Failed to initialize TTS engine")
        return None

def listen_to_speech():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration = 1)
            audio = recognizer.listen(source, phrase_time_limit= 10 )
        
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I don't catch you"
    except sr.RequestError:
        return "Speech service not available"
    except Exception as e:
        return f"ERROR: {e}"


def main():
    st.title("Personal Voice Assistant")
    st.markdown("---")

    # initialize session state for chatting
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content" : "You are a helpful voice assitant. Reply just one line"}
        ]

    # initialize the session messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Controls")

        tts_enabled = st.checkbox("Enable Text to Speech", value = True)

        # voice selection
        voice_gender = st.selectbox(
            "Voice Gender",
            options = ['Girl', 'Boy'],
            index = 1,
            help = "Choose Voice Type"
        )

        if st.button("Start Voice Input", type = "primary", use_container_width= True):
            with st.spinner("Listening..."):
                user_input = listen_to_speech()

if __name__ == "__main__":
    main()