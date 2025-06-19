# This code is a Streamlit application that generates patient education content using Ollama.
# It allows healthcare providers to input patient details and receive tailored educational material.
# It also includes a feature to convert the generated text into audio using gTTS (Google Text-to-Speech).
# In addition, it provides examples of responses for different medical conditions and personas.

# ------------------------------------------------------------------------------- Imports and Initialization -------------------------------------------------------------------------------

# Imports necessary libraries
import streamlit as st
import ollama
import re
from gtts import gTTS
from io import BytesIO

# Cache the audio generation by text (only re-run if the text changes)
@st.cache_resource(show_spinner=False)
def generate_tts_audio(text):
    tts = gTTS(text)
    audio_fp = BytesIO()           
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp

# Defines the default/initial input values and toggles for the session state
default_values = {
    "name": "",
    "age": "",
    "condition": "Select a condition...",
    "interest": "",
    "life_detail": "",
    "concern": "",
    "personal_toggle": False,
    "tts_toggle": False
}

# Checks if session state keys exist, if not, initializes them with default values
for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Clears all inputs by removing session state keys
def clear_inputs():
    for key, value in default_values.items():
        if key in st.session_state:
            del st.session_state[key]  # ✅ Remove instead of assigning
    st.rerun()

# Converts markdown text (text w/ formatting done automatically by Ollama) to plain text
def markdown_to_plaintext(markdown_text):
    # Remove headers
    text = re.sub(r'#+ ', '', markdown_text)
    # Remove bold and italics
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
    # Remove inline code
    text = re.sub(r'`(.+?)`', r'\1', text)
    # Remove links [text](url)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # Remove unordered list markers
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    # Remove extra newlines
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

# Validates input to ensure it contains only letters, numbers, and spaces
def control_input(input):
    if not re.match("^[a-zA-Z0-9 ]*$", input):
        st.error("Please use only letters, numbers, and spaces.")


# ------------------------------------------------------------------------------- Input and AI Generation -------------------------------------------------------------------------------

st.title("Patient Education Generator")

st.write("Please fill in the information below:")

# Creates input fields for patient details and condition selection
name = st.text_input("Enter the patient’s name:", key="name")
control_input(name)
age = st.text_input("Enter the patient’s age:", key="age")
control_input(age)
condition = st.selectbox(
    "Choose a condition:",
    ["Select a condition...", "Influenza", "Eczema", "Depression", "Back Pain", "Breast Cancer"],
    index=["Select a condition...", "Influenza", "Eczema", "Depression", "Back Pain", "Breast Cancer"].index(st.session_state["condition"]),
    key="condition"
)

personal_toggle = st.checkbox("Toggle personal details", key="personal_toggle")

# If the personal details toggle is on, show additional input fields for interests, life details, and concerns
if personal_toggle:
    interest = st.text_input("Enter one of the patient's interests (eg. sports, gardening, fashion):", key="interest")
    control_input(interest)
    life_detail = st.text_input("Enter a detail of the patient's life (eg. has children, works in an office):", key="life_detail")
    control_input(life_detail)
    concern = st.text_input("Enter the patient's concern (eg. worried about..., curious about...):", key="concern")
    control_input(concern)

tts_toggle = st.checkbox("Toggle text-to-speech", key="tts_toggle")

# Clears all inputs when the button is pressed
if st.button("Clear Inputs"):
    clear_inputs()

# Combines all user inputs into a single prompt
if personal_toggle:
    # Creates a prompt that includes personal details if the toggle is on
    user_prompt = f"You are talking to {name}, a {age} -year-old who was diagnosed with {condition}. They are interested in {interest}. They {life_detail} and are {concern}. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive."
else:
    # Creates a prompt without personal details if the toggle is off
    user_prompt = f"You are talking to {name}, a {age} -year-old who was diagnosed with {condition}. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language. Be kind and supportive."

# Generates patient education content when button is pressed
if st.button("Generate"):
    # Checks for empty fields, invalid conditions, or missing personal details if toggle is on
    if not name or not age:
        st.error("Please fill in all fields.")
    elif condition == "Select a condition...":
        st.error("Please select a condition.")
    elif personal_toggle and (not interest or not life_detail or not concern):
        st.error("Please fill in all personal detail fields or uncheck the box.")
    # If all inputs are valid, generate content
    else:
        with st.spinner("Please wait while content generates. This may take a minute..."):
            # In case of an error with Ollama, it will display an error message
            try:
                generation = ollama.generate(model='llama3', prompt=user_prompt)
                # Only the response part of the output, no metadata
                content = generation['response']
                generation_successful = True
                if st.button("Clear Response"):
                    st.rerun()
            except Exception as e:
                st.error(f"An error occurred while generating content: {str(e)}")
                generation_successful = False
        if generation_successful:
            # If text-to-speech toggle is on, generate audio and display content, else just display content
            if tts_toggle:
                with st.spinner("Please wait while audio generates. This may take a minute..."):
                    # creates new temp audio file in memory
                    sound_file = BytesIO()
                    plain = markdown_to_plaintext(content)
                    # creates a gTTS object with ollama output as text and english as language
                    tts = gTTS(plain, lang='en')
                    # puts the generated text to temp file
                    tts.write_to_fp(sound_file)
                    # streams temp file to streamlit ui for playing
                    st.audio(sound_file)
                    st.markdown(content)
            else:
                st.markdown(content)

# ------------------------------------------------------------------------------- Response Examples ------------------------------------------------------------------------------------

st.header("Examples:")

with st.expander('Asthma'):
    st.markdown("**Prompt:**")
    st.markdown("You are talking to Zoe, a 12 year-old who was diagnosed with Asthma. They are interested in playing the flute. They recently joined their school band and are worried that asthma attacks will stop them from performing. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive.")
    st.markdown("**Response:**")
    # Path to text file
    text_path = "example_text/asthma_text.md"
    # Open and read file
    with open(text_path, "r", encoding="utf-8") as file:
        explanation = file.read()
    # Path to audio file
    audio_path = "tts_audio/asthma_audio.mp3"
    # Open and read file as bytes
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    # Play audio
    st.audio(audio_bytes, format="audio/mp3")
    # Display text
    st.markdown(explanation)

with st.expander('Diabetes'):
    st.markdown("**Prompt:**")
    st.markdown("You are talking to Daniel, a 38 year-old who was diagnosed with Type 2 Diabetes. They are interested in cooking and trying new foods. They were recently told to change their eating habits and feel overwhelmed and unsure what they can eat now. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive.")
    st.markdown("**Response:**")
    # Path to text file
    text_path = "example_text/diabetes_text.md"
    # Open and read file
    with open(text_path, "r", encoding="utf-8") as file:
        explanation = file.read()
    # Path to audio file
    audio_path = "tts_audio/diabetes_audio.mp3"
    # Open and read file as bytes
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    # Play audio
    st.audio(audio_bytes, format="audio/mp3")
    # Display text
    st.markdown(explanation)

with st.expander('High Blood Pressure'):
    st.markdown("**Prompt:**")
    st.markdown("You are talking to Lillian, a 64 year-old who was diagnosed with High Blood Pressure. They are interested in playing with their grandchildren. They take their grandchildren to the park often and are worried that their condition could make them too tired or sick to keep up with them. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive.")
    st.markdown("**Response:**")
    # Path to text file
    text_path = "example_text/hypertension_text.md"
    # Open and read file
    with open(text_path, "r", encoding="utf-8") as file:
        explanation = file.read()
    # Path to audio file
    audio_path = "tts_audio/hypertension_audio.mp3"
    # Open and read file as bytes
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    # Play audio
    st.audio(audio_bytes, format="audio/mp3")
    # Display text
    st.markdown(explanation)