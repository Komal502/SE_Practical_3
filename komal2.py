import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile

# Page settings
st.set_page_config(page_title="Simple Text → Speech", layout="centered")

# Map full names to language codes
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr"
}

# Custom CSS
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 16px !important; }
    .stButton button {
        font-size: 18px !important;
        height: 3em !important;
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stDownloadButton button { font-size: 16px !important; border-radius: 8px !important; }
    .main { max-width: 650px; margin: auto; padding-top: 30px; }
    </style>
""", unsafe_allow_html=True)

st.title("🗣 Simple Text → Speech")
st.write("Enter text, optionally translate, then click Speak to generate audio.")

# Input
text = st.text_area("✏️ Enter text to speak:",
                    value="Hello! This is a simple Text to Speech prototype.", height=150)

# Translate option
use_translate = st.checkbox("🌐 Translate text before speaking (optional)")

if use_translate:
    src_lang_name = st.selectbox("Source language:", ["Auto Detect"] + list(LANGUAGES.keys()))
    tgt_lang_name = st.selectbox("Target language:", list(LANGUAGES.keys()))
else:
    src_lang_name = None
    tgt_lang_name = None

# Voice options
slow = st.checkbox("🐢 Speak slowly")
voice_lang_name = st.selectbox("🎤 Voice language for speech:", list(LANGUAGES.keys()))

# Translation preview
speak_text = text
if use_translate and tgt_lang_name and text.strip():
    try:
        src_lang_code = "auto" if src_lang_name == "Auto Detect" else LANGUAGES[src_lang_name]
        tgt_lang_code = LANGUAGES[tgt_lang_name]

        translated = GoogleTranslator(source=src_lang_code, target=tgt_lang_code).translate(text)
        speak_text = translated

        if src_lang_code == "auto":
            detected_lang = GoogleTranslator(source='auto', target='en').translate(text)
            st.info(f"Detected language: {detected_lang}")

        st.success(f"Preview translation: {speak_text}")

    except Exception as e:
        st.error(f"Translation error: {e}")

# Speak
if st.button("▶ Speak"):
    if not speak_text.strip():
        st.error("Please enter some text first.")
    else:
        try:
            voice_lang_code = LANGUAGES[voice_lang_name]
            tts = gTTS(text=speak_text, lang=voice_lang_code, slow=slow)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_name = fp.name
            tts.save(temp_name)

            st.audio(temp_name)
            with open(temp_name, "rb") as f:
                st.download_button("⬇ Download MP3", data=f, file_name="tts_output.mp3", mime="audio/mp3")

        except Exception as e:
            st.error(f"Error creating speech: {e}")
