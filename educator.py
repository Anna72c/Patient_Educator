# This code is a Streamlit application that generates patient education content using Ollama.
# It allows healthcare providers to input patient details and receive tailored educational material.
# It also includes a feature to convert the generated text into audio using gTTS (Google Text-to-Speech) and the ability to rewrite the response.
# In addition, it provides examples of responses for different medical conditions and personas.

# ------------------------------------------------------------------------------- Imports and Initialization -------------------------------------------------------------------------------

# Imports necessary libraries
import streamlit as st
from groq import Groq
import re
from gtts import gTTS
from io import BytesIO

# Connects to Groq API through API key in secrets
client = Groq(api_key=st.secrets["groq_api_key"])

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

# Session state initialization for content generation variables
# Initializes "generation_successful" to False
if "generation_successful" not in st.session_state:
    st.session_state["generation_successful"] = False
# Initializes "audio_successful" to False
if "audio_successful" not in st.session_state:
    st.session_state["audio_successful"] = False  
# Initializes "content" to an empty string
if "content" not in st.session_state:
    st.session_state["content"] = ""
# Initializes "rewritten" to an empty string.
if "rewritten" not in st.session_state:
    st.session_state["rewritten"] = ""
if "rewrite_successful" not in st.session_state:
    st.session_state["rewrite_successful"] = False

# Checks if session state keys exist, if not, initializes them with default values
for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Clears all inputs by removing session state keys
def clear_inputs():
    for key, value in default_values.items():
        if key in st.session_state:
            del st.session_state[key]  # Remove instead of assigning
    st.rerun()

# Clears previous generated response and resets status flags
def clear_response():
    if "generation_successful" in st.session_state:
        del st.session_state["generation_successful"]  # Remove instead of assigning
    if "audio_successful" in st.session_state:
        del st.session_state["audio_successful"]  # Remove instead of assigning
    if "rewrite_successful" in st.session_state:
        del st.session_state["rewrite_successful"]  # Remove instead of assigning
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

# Calls Ollama through Groq to generate a response
def generate(prompt):
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",  # Or "llama3-70b-4096" or the newer "llama-3.3-70b-versatile"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content.strip()

# ------------------------------------------------------------------------------- Input and AI Generation -------------------------------------------------------------------------------

st.title("Patient Education Generator")

st.write("Please fill in the information below:")

# Input fields for name, age, and condition
name = st.text_input("Enter the patient’s name:", key="name")
age = st.text_input("Enter the patient’s age:", key="age")
condition = st.selectbox(
    "Choose a condition:",
    ["Select a condition...", "Influenza", "Eczema", "Depression", "Back Pain", "Breast Cancer"],
    index=["Select a condition...", "Influenza", "Eczema", "Depression", "Back Pain", "Breast Cancer"].index(st.session_state["condition"]),
    key="condition"
)

# Toggle for including personal details
personal_toggle = st.checkbox("Toggle personal details", key="personal_toggle")

# If the personal details toggle is on, show additional input fields for interests, life details, and concerns
if personal_toggle:
    interest = st.text_input("Enter one of the patient's interests (eg. sports, gardening, fashion):", key="interest")
    life_detail = st.text_input("Enter a detail of the patient's life (eg. has children, works in an office):", key="life_detail")
    concern = st.text_input("Enter the patient's concern (eg. worried about..., curious about...):", key="concern")

# Toggle for text-to-speech
tts_toggle = st.checkbox("Toggle text-to-speech", key="tts_toggle")

# Button to clear all inputs
if st.button("Clear Inputs"):
    clear_inputs()

# Combines all user inputs into a single prompt, with or without personal details
if personal_toggle:
    # Creates a prompt that includes personal details if the toggle is on
    user_prompt = f"You are talking to {name}, a {age} -year-old who was diagnosed with {condition.lower()}. They are interested in {interest}. They {life_detail} and are {concern}. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive."
else:
    # Creates a prompt without personal details if the toggle is off
    user_prompt = f"You are talking to {name}, a {age} -year-old who was diagnosed with {condition.lower()}. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language. Be kind and supportive."

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
                st.session_state["content"] = generate(user_prompt)
                st.session_state["generation_successful"] = True
            except Exception as e:
                st.error(f"An error occurred while generating content: {str(e)}")
                generation_successful = False

# If generation was successful, display output
if st.session_state["generation_successful"]:
    # simplifies code
    content = st.session_state["content"]
    # If text-to-speech toggle is on, generate audio and display content, else just display content
    if tts_toggle and not st.session_state["audio_successful"]:
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
            st.session_state["audio_successful"] = True
            st.markdown(content)
    else:
        st.markdown(content)

    # Warns that text is AI generated
    st.markdown("*This explanation is AI generated and is not a substitute for medical advice. Please consult a healthcare professional for medical guidance.*")
    
    # Clears generated response
    if st.button("Clear Response"):
        clear_response()

# ------------------------------------------------------------------------------- Rewrite Option -------------------------------------------------------------------------------
# Once generation is complete, option to rewrite
if st.session_state["generation_successful"]:
    st.subheader("Want to change the tone or length?")

    # Selectbox for rewrite style
    style = st.selectbox(
        "Choose rewrite style:",
        ["Shorter", "Simpler", "Friendlier", "More Detailed", "Bullet Points", "Professional Tone"]
    )

    # Rewrite button
    if st.button("Rewrite Explanation"):
        st.session_state["rewrite_successful"] = False

        with st.spinner("Rewriting explanation..."):
            # Create a prompt based on selected style
            if style == "Bullet Points":
                rewrite_prompt = f"Rewrite the following explanation as clear bullet points:\n\n{content}"
            else:
                rewrite_prompt = f"Rewrite the following explanation to be {style.lower()}:\n\n{content}"
            try:
                st.session_state["rewritten"] = generate(rewrite_prompt)
                st.session_state["rewrite_successful"] = True
            except Exception as e:
                st.error(f"An error occurred during rewriting: {str(e)}")

    # if rewrite is successful, display rewrite and offer audio option
    if st.session_state["rewrite_successful"]:
        if st.button("Play Audio"):
            with st.spinner("Please wait while audio generates. This may take a minute..."):
                # creates new temp audio file in memory
                sound_file = BytesIO()
                plain = markdown_to_plaintext(st.session_state["rewritten"])
                # creates a gTTS object with ollama output as text and english as language
                tts = gTTS(plain, lang='en')
                # puts the generated text to temp file
                tts.write_to_fp(sound_file)
                # streams temp file to streamlit ui for playing
                st.audio(sound_file)
        st.markdown(st.session_state["rewritten"])

        # Warns that text is AI generated
        st.markdown("*This explanation is AI generated and is not a substitute for medical advice. Please consult a healthcare professional for medical guidance.*")

# ------------------------------------------------------------------------------- Response Examples ------------------------------------------------------------------------------------

# Spacing
st.text("")
st.text("")

st.subheader("Examples:")

st.markdown("These are sample AI-generated explanations for different patients. They show how the AI can personalize explanations based on age, lifestyle, and health needs.")

# Asthma Example
with st.expander('**Asthma**'):
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

# Diabetes Example
with st.expander('**Diabetes**'):
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

# High Blood Pressure (Hypertension) Example
with st.expander('**High Blood Pressure**'):
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