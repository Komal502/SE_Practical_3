# Trigger redeploy
import streamlit as st
from gtts import gTTS
from io import BytesIO
from googletrans import Translator

# --------------------
# Streamlit App Title
# --------------------
st.set_page_config(page_title="Text-to-Speech Translator", page_icon="🔊", layout="centered")
st.title("🔊 Text-to-Speech with Translation")
st.markdown("Convert text to speech with optional translation. Type text or upload a file.")

# --------------------
# Language Options
# --------------------
# Format: short_code: Full name
languages = {
    'en': 'English', 'hi': 'Hindi', 'mr': 'Marathi', 'gu': 'Gujarati', 'ta': 'Tamil', 'te': 'Telugu',
    'bn': 'Bengali', 'pa': 'Punjabi', 'ur': 'Urdu', 'kn': 'Kannada', 'ml': 'Malayalam', 'fr': 'French',
    'es': 'Spanish', 'de': 'German', 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese (Simplified)'
}

# Dropdowns
src_lang = st.selectbox("Source Language (text language)", options=languages.keys(), format_func=lambda x: languages[x])
target_lang = st.selectbox("Target Language (for speech)", options=languages.keys(), format_func=lambda x: languages[x])

# --------------------
# Text Input Section
# --------------------
text_input = st.text_area("Enter your text here:")

uploaded_file = st.file_uploader("Or upload a text file (.txt)", type=["txt"])
if uploaded_file is not None:
    text_input = uploaded_file.read().decode("utf-8")

# --------------------
# Generate TTS
# --------------------
if st.button("Convert to Speech"):
    if text_input.strip() == "":
        st.warning("Please enter some text or upload a file.")
    else:
        try:
            # Translate text if needed
            translator = Translator()
            if src_lang != target_lang:
                translated = translator.translate(text_input, src=src_lang, dest=target_lang).text
            else:
                translated = text_input

            # Convert to speech
            tts = gTTS(text=translated, lang=target_lang)
            audio_data = BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)

            # Play audio
            st.audio(audio_data, format="audio/mp3")

            # Download link
            st.download_button(
                label="⬇️ Download Audio",
                data=audio_data,
                file_name="speech.mp3",
                mime="audio/mp3"
            )

            # Show translated text
            st.success(f"Translated Text ({languages[target_lang]}):")
            st.write(translated)

        except Exception as e:
            st.error(f"Error: {str(e)}")
