**Patient Education Generator  
_Project Documentation_**

**Anna Hoen  
SciEncephalon AI  
June – July 2025**

**Introduction**

The Patient Education Generator is an AI-powered web app designed to provide clear, personalized medical explanations. This project addresses the challenge many patients and caregivers face when trying to understand complex, jargon-heavy medical information. By generating empathetic, easy-to-understand explanations tailored to individual patient details, the app aims to improve health literacy, patient confidence, and ultimately treatment outcomes.

**The Problem**

Medical information is often difficult to understand because it is complex, impersonal, and full of specialized terminology. Many patients and caregivers struggle to grasp their diagnoses and treatment plans, which can lead to confusion, anxiety, and poor adherence to medical advice. According to the National Institute of Health, clear and empathetic education significantly enhances patient understanding and health outcomes.

**Understanding the Users**

The app primarily helps three groups:

- **Patients**, who need simple and clear explanations of their medical conditions
- **Caregivers**, who support patients and need guidance to manage and explain medical information
- **Healthcare workers**, who seek efficient ways to communicate diagnoses and treatment details clearly

**The Solution**

To address these challenges, I developed a personalized AI-powered education app. This web-based tool generates patient-specific explanations using AI, incorporating patient details such as name, age, and lifestyle. It also features text-to-speech functionality to make the explanations more accessible.

**Technical Implementation**

The app was built using Streamlit, a Python framework for creating web apps. It integrates AI language generation models to produce clear explanations and leverages text-to-speech (gTTS) for audio output. The user interface includes form inputs for condition details and toggles for personalization and caregiver mode, as well as buttons to generate and rewrite explanations.

**AI Model Choice**

For AI generation, I used LLaMA 3 (8B) because it is open-source, fast, and offers a good balance of performance and size. Compared to alternatives, it is more tested and has less bugs than LLaMA 4 and provides more complex reasoning than Mistral. For deployment, I switched from Ollama running locally to Groq, which offers online access with fast response times while using the same prompting structure and model availability as Ollama, requiring no additional learning or model changes.

**Prompting Strategy**

Prompt engineering was crucial to producing empathetic and clear responses. The base prompt includes patient name, age, and condition. An optional personalization toggle allows adding interests, lifestyle details, and specific concerns to make explanations more relatable. I designed rewrite prompts to adjust the output’s tone and format—such as converting paragraphs into bullet points or making the language friendlier and more concise—by feeding the AI the original text and instructions on how to revise it.

**Features and User Interface**

The app features a user input form with toggles for personalization and caregiver mode. It includes buttons to generate new explanations, rewrite existing ones with different tones or styles, and clear inputs or responses. The text-to-speech integration reads the explanations aloud to users. To showcase the app’s capabilities, sample outputs were created for asthma, diabetes, and high blood pressure.

**Future Possibilities**

There are several potential enhancements to the project:

- Adding PDF export or print functionality to make it easier for patients to save and share explanations
- Improving the text-to-speech model for more natural and varied audio output
- Expanding personalization with multilingual support and a comprehensive condition list instead of an “other” category
- Enhancing user interaction by collecting feedback to improve explanations and implementing a conversational interface for follow-up questions

**Lessons Learned**

Throughout this project, I gained valuable technical and soft skills:

- I learned to use key tools such as Streamlit, Ollama, Groq, and GitHub
- I developed a deeper understanding of AI concepts including language models, prompt engineering, and text-to-speech
- I improved my programming skills, especially in Python and Visual Studio Code
- Beyond technical growth, I enhanced my time management, problem-solving, communication, and adaptability skills through project management and independent work

**Important Links**

Live App: [anna72c-patient-educator.streamlit.app](https://anna72c-patient-educator.streamlit.app/)

GitHub Repo: [](https://github.com/Anna72c/Patient_Educator)[Anna72c/Patient_Educator](https://github.com/Anna72c/Patient_Educator)

Tools and Platforms:

- [LLaMA 3 by Meta](https://ai.meta.com/blog/meta-llama-3/)
- [Streamlit](https://streamlit.io)
- [Ollama](https://ollama.com/)
- [Groq](https://groq.com)
- [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)
