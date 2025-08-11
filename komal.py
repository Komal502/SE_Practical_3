import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import os

# Page settings
st.set_page_config(page_title="Simple Text → Speech", layout="centered")

# Custom CSS for better look
st.markdown("""
    <style>
    .stTextArea textarea {
        font-size: 16px !important;
    }
    .stButton button {
        font-size: 18px !important;
        height: 3em !important;
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stDownloadButton button {
        font-size: 16px !important;
        border-radius: 8px !important;
    }
    .main {
        max-width: 650px;
        margin: auto;
        padding-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗣 Simple Text → Speech")
st.write("Enter text, optionally translate, then click Speak to generate audio.")

# Input area
text = st.text_area("✏️ Enter text to speak:", 
                    value="Hello! This is a simple Text to Speech prototype.", height=150)

# Translate option
use_translate = st.checkbox("🌐 Translate text before speaking (optional)")

if use_translate:
    src_lang = st.selectbox("Source language:", ["auto", "en", "hi", "es", "fr"], index=0)
    tgt_lang = st.selectbox("Target language:", ["en", "hi", "es", "fr"], index=0)
else:
    src_lang = None
    tgt_lang = None

# Voice options
slow = st.checkbox("🐢 Speak slowly")
lang_for_gtts = st.selectbox("🎤 Voice language for speech:", ["en", "hi", "es", "fr"], index=0)

# Show translation preview in real-time
speak_text = text
if use_translate and tgt_lang and text.strip():
    try:
        if src_lang == "auto":
            translated = GoogleTranslator(source='auto', target=tgt_lang).translate(text)
            detected_lang = GoogleTranslator(source='auto', target='en').translate(text)  # quick detect
            st.info(f"Detected language: {detected_lang}")
        else:
            translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
        speak_text = translated
        st.success(f"Preview translation: {speak_text}")
    except Exception as e:
        st.error(f"Translation error: {e}")

# Speak button
if st.button("▶ Speak"):
    if not speak_text.strip():
        st.error("Please enter some text first.")
    else:
        try:
            # Create speech
            tts = gTTS(text=speak_text, lang=lang_for_gtts, slow=slow)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_name = fp.name
            tts.save(temp_name)

            # Play audio
            st.audio(temp_name)

            # Download option
            with open(temp_name, "rb") as f:
                st.download_button("⬇ Download MP3", data=f, file_name="tts_output.mp3", mime="audio/mp3")

        except Exception as e:
            st.error(f"Error creating speech: {e}")
