import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from gtts.lang import tts_langs
from pathlib import Path
import tempfile

# --- Setup ---
st.set_page_config(page_title="Multilingual Translator & Accessibility Tool", layout="centered")

st.title("🌍 Multilingual Translator with Source Language Detection")

# --- Extended Language Dictionary ---
languages = {
    'Auto Detect': 'auto',
    'English': 'en',
    'French': 'fr',
    'Spanish': 'es',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Urdu': 'ur',
    'Turkish': 'tr',
    'Persian (Farsi)': 'fa',
    'Greek': 'el',
    'Dutch': 'nl',
    'Polish': 'pl',
    'Czech': 'cs',
    'Slovak': 'sk',
    'Romanian': 'ro',
    'Hungarian': 'hu',
    'Swedish': 'sv',
    'Norwegian': 'no',
    'Danish': 'da',
    'Finnish': 'fi',
    'Hebrew': 'he',
    'Thai': 'th',
    'Vietnamese': 'vi',
    'Filipino (Tagalog)': 'tl',
    'Malay': 'ms',
    'Swahili': 'sw',
    'Zulu': 'zu',
    'Amharic': 'am',
    'Somali': 'so',
    'Igbo': 'ig',
    'Yoruba': 'yo',
    'Hausa': 'ha',
}

# --- Source Language Selection (Auto vs Manual) ---
st.subheader("🌐 Choose Source Language Mode")
mode = st.radio("How do you want to set source language?", ["Automatic Detection", "Manual Selection"])

if mode == "Manual Selection":
    src_lang_choice = st.selectbox("Select source language:", list(languages.keys())[1:])
    source_lang_code = languages[src_lang_choice]
else:
    source_lang_code = "auto"

# --- Target Language ---
target_lang_choice = st.selectbox("Select target language:", list(languages.keys())[1:])
target_lang_code = languages[target_lang_choice]

# --- gTTS Supported ---
gtts_supported = tts_langs()
TTS_OVERRIDES = {"zh-CN": "zh-CN", "zh-TW": "zh-TW"}

def get_tts_lang(code: str):
    tts_code = TTS_OVERRIDES.get(code, code)
    return tts_code if tts_code in gtts_supported else None

def speak(text: str, preferred_code: str):
    temp_path = Path(tempfile.gettempdir()) / "output.mp3"
    try:
        lang_for_tts = get_tts_lang(preferred_code)
        if lang_for_tts is None:
            st.info("🔈 TTS not available for this language. Using English instead.")
            lang_for_tts = "en"
        gTTS(text, lang=lang_for_tts).save(str(temp_path))
        return temp_path
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

# --- Text Translation ---
st.subheader("⌨️ Type and Translate")
user_text = st.text_area("Enter text to translate:")

if st.button("Translate Text"):
    if user_text.strip():
        try:
            translated = GoogleTranslator(source=source_lang_code, target=target_lang_code).translate(user_text)
            
            st.write(f"**Translated ({target_lang_choice}):** {translated}")

            audio_path = speak(translated, target_lang_code)
            if audio_path:
                st.audio(str(audio_path))
        except Exception as e:
            st.error(f"Translation error: {e}")
    else:
        st.warning("⚠️ Please enter some text first.")

