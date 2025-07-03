from gtts import gTTS
from io import BytesIO
import re
import markdown

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

with open("asthma_explanation.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()

plain_text = markdown_to_plaintext(markdown_text)

tts = gTTS(plain_text, lang='en')
tts.save("asthma_audio.mp3")
