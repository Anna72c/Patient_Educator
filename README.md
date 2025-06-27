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

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Anna72c/Patient_Educator.git
   cd Patient-Educator

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Add your Groq API key to .streamlit/secrets.toml:
   ```toml
   groq_api_key = "your_api_key_here"

4. Run the app:
   ```bash
   streamlit run app.py

## Project Structure
- app.py                # Main Streamlit application
- example_text          # Example AI explanations (Markdown)
  - asthma_text.md
  - diabetes_text.md
  - hypertension_text.md
- tts_audio             # Pre-generated audio files
  - asthma_audio.mp3
  - diabetes_audio.mp3
  - hypertension_audio.mp3
- .streamlit
  - secrets.toml        # API key storage

## Future Ideas
- More conditions and audio languages
- User feedback collection
- PDF download button
- Caregiver mode toggle

## Made By
**Anna Hoen**

Mentor: Neelima

Project: SciEncephalon Summer 2025 Internship – *Patient Education Generator*