# app.py - Simple TTS prototype using Streamlit + gTTS + deep-translator
import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import os

st.set_page_config(page_title="Simple TTS Prototype", layout="centered")
st.title("Simple Text → Speech Prototype")
st.write("Type text, (optionally translate), then click Speak to generate audio.")

# Input area
text = st.text_area(
    "Enter text to speak:",
    value="Hello! This is a simple Text to Speech prototype.",
    height=150
)

# Translate option
use_translate = st.checkbox("Translate text before speaking (optional)")

if use_translate:
    src_lang = st.selectbox(
        "Source language (what you typed):",
        ["auto", "en", "hi", "es", "fr"],
        index=0
    )
    tgt_lang = st.selectbox(
        "Target language (voice will speak this):",
        ["en", "hi", "es", "fr"],
        index=0
    )
else:
    src_lang = None
    tgt_lang = None

# Voice options
slow = st.checkbox("Speak slowly (check for slow speed)")
lang_for_gtts = st.selectbox(
    "Voice language for speech:",
    ["en", "hi", "es", "fr"],
    index=0
)

if st.button("Speak"):
    if not text.strip():
        st.error("Please enter some text first.")
    else:
        try:
            speak_text = text
            if use_translate and tgt_lang:
                # Translate text using deep-translator
                if src_lang == "auto":
                    translated = GoogleTranslator(source='auto', target=tgt_lang).translate(text)
                else:
                    translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
                speak_text = translated
                st.write("Translated text:", speak_text)

            # Create speech
            tts = gTTS(text=speak_text, lang=lang_for_gtts, slow=slow)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_name = fp.name
            tts.save(temp_name)

            # Show audio player
            st.audio(temp_name)

            # Download link
            with open(temp_name, "rb") as f:
                st.download_button(
                    "Download MP3",
                    data=f,
                    file_name="tts_output.mp3",
                    mime="audio/mp3"
                )

        except Exception as e:
            st.error("Error creating speech: " + str(e))
            st.write("If translation or speech fails, check your internet connection.")
