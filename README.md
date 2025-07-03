# Patient Education Generator

This is a Streamlit web app designed to generate clear, personalized explanations of medical conditions for patients. It uses AI (via the Groq API) to simplify complex information and optionally converts it into speech using Google Text-to-Speech.

## Purpose
The tool helps patients understand their diagnoses by adjusting explanations to fit their age, interests, concerns, and lifestyle. It’s especially useful for pediatric, elderly, or health-anxious users.

## Features
- Input name, age, and condition
- Optional personalization: hobbies, lifestyle, concerns
- AI-generated explanation using llama3
- Toggle for text-to-speech audio
- Rewrite the output in different tones (simpler, professional, bullet points, etc.)
- Examples with text and audio for:
  - Asthma
  - Diabetes
  - High Blood Pressure

## Tech Stack
- **Frontend**: Streamlit
- **AI**: Groq + Ollama llama3:8b model
- **Speech**: gTTS (Google Text-to-Speech)
- **Languages**: Python, Markdown
- **Other tools**: VS Code, GitHub, ChatGPT

## Try It Online
Check out the live demo here: [Patient Education Generator](https://anna72c-patient-educator.streamlit.app/)

No installation or setup needed — just open the app and try it!

How to Use:

  1. Enter patient details (name, age, condition)

  2. (Optional) Add personal information or enable caregiver mode

  3. Click "Generate" to receive a tailored explanation

  4. Use "Rewrite" for different tones or formats

  5. Enable text-to-speech to hear the explanation

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Anna72c/Patient_Educator.git
   cd Patient-Educator

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Get a free Groq API key:
   - Go to [https://console.groq.com/keys](https://console.groq.com/keys)
   - Create a key and copy it

4. Create a `.streamlit` folder and add a `secrets.toml` file with:
   ```toml
   groq_api_key = "your_key_here"

5. Run the app:
   ```bash
   streamlit run educator.py

## Project Structure
- .devcontainer         (VS Code Dev Container)
  - devcontainer.json
- example_text          (Example AI explanations)
  - asthma_text.md
  - diabetes_text.md
  - hypertension_text.md
- tts_audio             (Pre-generated audio files)
  - asthma_audio.mp3
  - diabetes_audio.mp3
  - hypertension_audio.mp3
- README.md             (This file)
- docs.md               (Full project documentation)
- educator.py           (Main Streamlit application)
- requirements.txt      (Required dependencies)

## Future Ideas
- More conditions
- User feedback collection
- PDF download button
- Caregiver mode toggle

## Made By
**Anna Hoen**

Mentor: Neelima

Project: SciEncephalon Summer 2025 Internship – *Patient Education Generator*
