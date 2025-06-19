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
    markdown_text = """
Hi Zoe! I'm so glad you're excited about playing the flute in your school band! I know it can be scary to worry about having asthma and performing, but don't worry, we'll get through this together!

So, what is asthma? Asthma is a chronic condition that affects the airways in our lungs. It's like when you try to blow up a balloon, but it gets stuck and hard to inflate. For people with asthma, their airways can get swollen and constricted, making it harder for air to flow through.

Now, let me explain why you might be more likely to have an asthma attack while playing the flute. When you breathe in deeply and rapidly while playing your instrument, it can trigger your airways to become inflamed and narrow. This is because your body is trying to protect itself from the sudden change in breathing patterns. It's like when you're running really fast and your lungs get a little tired – they need time to recover!

So, what are the symptoms of an asthma attack? If you experience any of these, it means your airways are getting irritated:

- **Wheezing**: Listen for that funny sound in your chest or throat when you breathe.  
- **Coughing**: You might cough a lot more than usual, especially at night.  
- **Shortness of breath**: You might feel like you're not getting enough air, even if you're just sitting still.  
- **Chest tightness**: It feels like someone's squeezing your chest really hard.  

Now, let me tell you about the good news! There are many ways to manage and treat asthma. Here are some super cool treatment options:

- **Inhalers**: These are special devices that help relax your airways and make it easier to breathe. You might need an inhaler with a quick-relief medicine (like albuterol) for sudden attacks, or one with long-term control medication (like fluticasone).  
- **Medications**: Your doctor might prescribe pills or liquids to help prevent attacks.  
- **Breathing exercises**: Deep breathing can help slow down your heart rate and calm you down when you're feeling anxious.  
- **Avoiding triggers**: Try to stay away from things that make your asthma worse, like strong smells, pollen, or dust.  

Here's a fun example: Imagine you're playing the flute in front of an audience, and suddenly you start to feel short of breath. You take out your inhaler, breathe in slowly, and puff out some medicine. It's like hitting the perfect note – it makes all the difference!

Some things you can do to help manage your asthma while playing the flute:

- **Take deep breaths**: Before you start playing, take a few slow, deep breaths in through your nose and out through your mouth.  
- **Use your inhaler before performing**: If your doctor recommends it, use your quick-relief medicine 15–30 minutes before you play to help prevent an attack.  
- **Stay hydrated**: Drink plenty of water or other fluids to keep your airways moist and healthy.  
- **Take breaks**: If you start feeling wheezy or tired, take a break and rest for a bit.  

I know it might seem like a lot to remember, but trust me, Zoe – with some practice and the right treatment, you'll be playing that flute like a pro in no time! You're not alone, and there are plenty of people who have successfully managed their asthma while pursuing their passions. You got this!

Remember, your health is super important, and it's okay to take care of yourself. If you ever feel scared or unsure about something, don't hesitate to talk to your parents, doctor, or a trusted friend.

Keep being awesome, Zoe!
"""
    asthma_text = markdown_to_plaintext(markdown_text)
    if st.button("🔊 Listen", key="asthma_audio"):
        with st.spinner("Please wait while audio loads. This may take a minute..."):
            audio_data = generate_tts_audio(asthma_text)
            st.audio(audio_data, format="audio/mp3")
    st.markdown(markdown_text)

with st.expander('Diabetes'):
    st.markdown("**Prompt:**")
    st.markdown("You are talking to Daniel, a 38 year-old who was diagnosed with Type 2 Diabetes. They are interested in cooking and trying new foods. They were recently told to change their eating habits and feel overwhelmed and unsure what they can eat now. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive.")
    st.markdown("**Response:**")
    markdown_text = """
Daniel! I'm here for you, and I want to help you navigate this new chapter with diabetes. Let's break it down together.
                
**What is diabetes?**
                
Diabetes is a condition where your body has trouble regulating blood sugar levels. There are two main types: Type 1 (autoimmune) and Type 2 (insulin resistance). Since you're newly diagnosed, I'm assuming you have Type 2 diabetes, which accounts for most cases.

**What causes Type 2 diabetes?**
                
In Type 2 diabetes, your body becomes resistant to insulin, a hormone that regulates blood sugar. This can be due to:
                
- Genetics: You may inherit a tendency from your parents.    
- Lifestyle factors: Being overweight or inactive, consuming too much sugar and refined carbohydrates, and not getting enough physical activity.            
- Other medical conditions: Certain health issues, like polycystic ovary syndrome (PCOS) or sleep apnea. 
                             
**What are the symptoms of Type 2 diabetes?**

Common signs include:
                
- Increased thirst and urination 
- Fatigue 
- Blurred vision 
- Slow healing of cuts and wounds 
- Frequent infections 
                
As a food enthusiast, you might be concerned about how these changes affect your cooking and eating habits. Rest assured, there are many delicious options available!

**What are the treatment options for Type 2 diabetes?**
                
To manage your condition, we'll focus on lifestyle changes and, if necessary, medication or insulin therapy.
                
- Dietary changes: Focus on whole, unprocessed foods like:            
  - Vegetables: Leafy greens, bell peppers, sweet potatoes 
  - Fruits: Berries, citrus fruits, apples 
  - Whole grains: Brown rice, quinoa, whole wheat bread 
  - Lean proteins: Chicken, fish, beans, lentils 
  - Healthy fats: Avocado, nuts, olive oil 
                
- Physical activity: Aim for at least 150 minutes of moderate-intensity exercise or 75 minutes of vigorous-intensity exercise per week. You can try:           
  - Brisk walking 
  - Swimming 
  - Cycling 
  - Yoga (if you have mobility concerns) 
                
- Medication and insulin therapy: If lifestyle changes alone aren't enough to regulate your blood sugar, we might discuss medication or insulin therapy. 
                
Additional tips for living with diabetes:
                
- Monitor your blood sugar levels regularly: Use a glucometer to track your levels and adjust your diet and activity accordingly. 
                
- Stay hydrated: Drink plenty of water throughout the day to help control blood sugar spikes. 
                
- Get enough sleep: Aim for 7-8 hours of restful sleep per night to support glucose regulation. 
                
- Manage stress: Practice stress-reducing techniques like meditation, deep breathing, or journaling. 

You are not alone!
                
As you navigate this new chapter, remember that you're not alone. Many people with diabetes have successfully managed their condition and enjoyed a fulfilling life. I'm here to support you every step of the way!

Let's work together to create a personalized plan that incorporates your love for cooking and trying new foods. We'll explore delicious recipes, meal planning strategies, and healthy habits to help you thrive with diabetes.

You got this, Daniel!              
"""
    diabetes_text = markdown_to_plaintext(markdown_text)
    if st.button("🔊 Listen", key="diabetes_audio"):
        with st.spinner("Please wait while audio loads. This may take a minute..."):
            audio_data = generate_tts_audio(diabetes_text)
            st.audio(audio_data, format="audio/mp3")
    st.markdown(markdown_text)

with st.expander('High Blood Pressure'):
    st.markdown("**Prompt:**")
    st.markdown("You are talking to Lillian, a 64 year-old who was diagnosed with High Blood Pressure. They are interested in playing with their grandchildren. They take their grandchildren to the park often and are worried that their condition could make them too tired or sick to keep up with them. Provide a detailed explanation of their condition, its causes, symptoms, and treatment options. Use simple language and include examples relevant to their interests and life details. Be kind and supportive.")
    st.markdown("**Response:**")
    markdown_text = """
Dear Lillian, I'm so glad you're interested in playing with your grandchildren! It's wonderful that you want to be a part of their lives and create memories together.
                
Now, let's talk about this thing called hypertension. Don't worry, I'll explain it in a way that's easy to understand, and we can even use some examples related to your love for the park!
                
Hypertension, or high blood pressure, is when the force of blood pushing against the walls of your blood vessels becomes too strong. Imagine the water flowing through a hose – if the hose gets clogged or narrowed, the water pressure increases. That's kind of what happens with hypertension.
                
**Causes:** Some common causes of hypertension include:
- Family history: If your parents or grandparents had high blood pressure, you might be more likely to develop it too. 
- Lifestyle factors: Being overweight or obese, not exercising regularly, and eating a diet that's too salty or fatty can all contribute to high blood pressure. 
- Medications: Certain medications, like birth control pills or decongestants, can raise blood pressure. 

**Symptoms:** The thing is, hypertension often doesn't cause any noticeable symptoms. It's like having a "silent friend" inside your body! But, if it gets too high, you might start to notice some issues, such as:
- Headaches 
- Dizziness or lightheadedness 
- Numbness or tingling in your hands and feet 
- Fatigue (feeling tired or weak) 
- Blurred vision 
                
**Treatment options:** Don't worry, there are many ways to manage hypertension! Some common treatments include:
- Medications: Your doctor might prescribe medications like diuretics, beta blockers, or ACE inhibitors to help lower your blood pressure. 
- Lifestyle changes: Eating a healthy diet that's low in salt and fat, exercising regularly (like taking those grandkids to the park!), and managing stress can all help reduce blood pressure. 
- Home monitoring: You can use a blood pressure monitor at home to track your readings and make adjustments as needed. 
                
Now, let's talk about how this affects you and playing with your grandchildren!
                
Fatigue is one of the symptoms of hypertension, so it's understandable that you might feel more tired than usual when playing with the kids. Dizziness or lightheadedness could be a concern if you're not careful - but with some simple precautions like taking breaks and staying hydrated, you can minimize those risks. Here are some tips to help you enjoy your time with the grandkids while managing your hypertension:
- Start slow: Don't overexert yourself when playing with the kids. Take breaks and pace yourselves. 
- Stay hydrated: Drink plenty of water before, during, and after playtime to keep your blood pressure in check. 
- Choose gentle activities: Opt for games or activities that don't require too much physical exertion, like board games, reading together, or even just having a picnic. 

Remember, Lillian, you're not alone! Many people with hypertension lead active, fulfilling lives and enjoy time with their loved ones. By making some simple lifestyle changes and working with your doctor, you can manage your condition and continue to be an amazing grandma!

How does that sound? Do you have any questions or concerns?        
"""
    hypertension_text = markdown_to_plaintext(markdown_text)
    if st.button("🔊 Listen", key="hypertension_audio"):
        with st.spinner("Please wait while audio loads. This may take a minute..."):
            audio_data = generate_tts_audio(hypertension_text)
            st.audio(audio_data, format="audio/mp3")
    st.markdown(markdown_text)