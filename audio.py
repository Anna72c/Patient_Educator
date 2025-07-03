from gtts import gTTS
from bs4 import BeautifulSoup
import markdown

with open("asthma_explanation.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()

html_text = markdown.markdown(markdown_text)
plain_text = BeautifulSoup(html_text, "html.parser").get_text()

tts = gTTS(plain_text)
tts.save("asthma_audio.mp3")
